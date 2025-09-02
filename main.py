from openai import OpenAI
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

system_prompt = """
You are an expert in interpreting the preferred job position/role based on user input.
Only output a clear job position to be used for Google search.
"""

user_query = input('Enter your preferred role or company: ')

response = client.responses.create(
    model='gpt-5-nano',
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
)

ai_response = response.output_text
print(f'AI response: {ai_response}')