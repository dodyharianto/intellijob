import os
from openai import OpenAI
from datetime import datetime
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from rag import retrieve_chunks
from job_search import scrape_google_jobs
import operator

client = OpenAI()

@tool
def analyze_documents(query: str):
    """
    Searches the user's personal documents (resume, portfolio) 
    to answer questions about their background or find relevant projects or experience.
    Use this to answer questions like "what projects do I have for this job?".
    """
    print(f"--- Analyzing Document ---")
    chunks = retrieve_chunks(collection_name='personal_docs', 
                             query=query, 
                             k=3)
    return f'Retrieved context from documents: {chunks}'

@tool
def search_for_jobs(query: str):
    """
    Searches Google Jobs in Singapore for a specific job title or company.
    Use this for any request related to finding new job postings.
    """
    print(f"--- Calling Job Search (SerpApi) ---")
    
    jobs_results_df = scrape_google_jobs(query=query)
    print(f"Found {len(jobs_results_df)} jobs.")
    return jobs_results_df

@tool
def search_google(query: str):
    """
    Searches Google for more detailed information, or for recent events.
    Use this for request related to relevant events based on user profile, general information of a company, or anything recent that you don't know.
    """
    print(f"--- Searching Google ---")

    today_date = datetime.today().strftime('%Y-%m-%d')
    context = [
        {
            "role": "system", 
            "content": f"Your task is to perform Google search. For your information, today date is {today_date}"},
        {
            "role": "user", 
            "content": query
        }
    ]
    print(f'context: {context}')
    response = client.responses.create(
        model="gpt-4o-mini",
        tools=[{
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": "SG",
                "city": "Singapore",
                "region": "Singapore",
            }
        }],
        input=context,
    )
    return response.output_text

tools = [analyze_documents, search_for_jobs, search_google]
tool_node = ToolNode(tools)

llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0
)
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[List, operator.add]

def call_llm(state: State):
    print('--- Calling LLM --- ')
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {'messages': [response]}

def call_tools(state: State):
    print('--- Calling a Tool ---')
    tool_outputs = tool_executor.invoke(state['messages'][-1].tool_calls)
    print(tool_outputs)

    return {'messages': tool_messages}

def make_decision(state: State):
    if state['messages'][-1].tool_calls:
        return 'call_tools'
    else:
        return 'end'

def build_workflow():
    workflow = StateGraph(State)

    workflow.add_node('llm', call_llm)
    workflow.add_node('tools', tool_node)
    workflow.set_entry_point('llm')

    workflow.add_conditional_edges(
        'llm',
        make_decision,
        {
            'call_tools': 'tools',
            'end': END
        }
    )

    # Return to LLM after calling tools
    workflow.add_edge('tools', 'llm')

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app

print(search_google('any networking events soon?'))