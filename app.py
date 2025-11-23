import chainlit as cl
from langchain_core.messages import SystemMessage, HumanMessage, AIMessageChunk
import chainlit as cl
import os
from datetime import datetime
from dotenv import load_dotenv
from orchestrator import build_workflow

app = build_workflow()

today_date = datetime.today().strftime('%Y-%m-%d')
SYSTEM_PROMPT = f"""
You are an expert in helping user finding the most relevant jobs based on their resume and portfolio.

You have access to the following tools:
1. analyze_documents(query): retrieves text chunks from the user's embeddings database (their resume, portfolio, or other files).
2. search_for_jobs(query): searches job postings in Singapore using Google Jobs API.
3. search_google(query): performs general-purpose web search.

Decide correctly when to call a tool.

Use analyze_documents:
- when asked about files, documents, resume, portfolio, projects.
Use search_for_jobs:
- when asked about jobs or companies.
Use search_google:
- when asked about recent events, or something that needs Google search.

For your information, today date is {today_date}
"""

@cl.set_starters
async def starters():
    return [
        cl.Starter(
            label='Search for jobs based on my profile',
            message='Search for jobs based on my profile',
            icon="/public/job.png"
        ),
        cl.Starter(
            label='Find data science workshops',
            message='Data science workshops',
            icon="/public/networking.png"
        ),
        cl.Starter(
            label=' Summarize my projects',
            message='Summarize the projects listed on my portfolio',
            icon="/public/summary.png"
        ),
    ]

@cl.on_message
async def main(message: cl.Message):
    """Process incoming user messages and stream back the AI's response."""
    ai_response = cl.Message(content='')
    await ai_response.send()

    config = {'configurable': {'thread_id': cl.context.session.thread_id}}
    input_message = {
        'messages': [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message.content)
        ]
    }

    for msg, _ in app.stream(input_message, config, stream_mode='messages'):
        if isinstance(msg, AIMessageChunk):
            ai_response.content += msg.content
            await ai_response.update()
