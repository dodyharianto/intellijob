from openai import OpenAI
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from memory import add_message, get_chat_history
from rag import embed_documents, retrieve_chunks
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
client = OpenAI()

default_system_prompt = """
You are an expert in helping user finding the most relevant jobs based on their resume and portfolio.
"""

def main_chat():
    collection_name = 'personal_docs'
    while True:
        chat_history = get_chat_history(n_messages=5)
        user_query = input("You [press 'Q' to quit]: ")
        if user_query.lower() == 'q':
            break
        add_message(role='user', message=user_query)

        retrieved_chunks = retrieve_chunks(collection_name, user_query, k=3)
        print(f'Most relevant chunks: {retrieved_chunks}')

        system_prompt = f"""
        {default_system_prompt}

        You know that:
        {retrieved_chunks}

        You have access to the past conversation:
        {chat_history}
        """
        print(f'System prompt: {system_prompt}')

        response = client.responses.create(
            model='gpt-5-nano',
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )
        
        ai_response = response.output_text
        print(f'IntelliJob💡: {ai_response}')
        add_message(role='assistant', message=ai_response)

main_chat()