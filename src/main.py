from openai import OpenAI
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from memory import add_message, get_chat_history
from rag import embed_documents, retrieve_chunks
from langchain_core.messages import SystemMessage, HumanMessage
from orchestrator import build_workflow

load_dotenv()
client = OpenAI()

default_system_prompt = """
You are an expert in helping user finding the most relevant jobs based on their resume and portfolio.
"""

def main():
    app = build_workflow()
    config = {"configurable": {"thread_id": "my-first-thread"}}
    while True:
        user_query = input("You [press 'Q' to quit]: ")
        if user_query.lower() == 'q':
            break
        
        events = app.stream(
            {"messages": [HumanMessage(content=user_query)]}, 
            config,
            stream_mode="values"
        )
        
        final_state = None
        for event in events:
            final_state = event

        if final_state:
            final_answer = final_state["messages"][-1].content
            print(f"\nIntelliJob💡: {final_answer}\n")

if __name__ == '__main__':
    main()