from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY') 

client = OpenAI()

def get_search_query():
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

    search_query = response.output_text
    return search_query

def scrape_google_jobs():
    query = get_search_query()
    search_params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "location": "Singapore",
        "api_key": SERPAPI_API_KEY
    }

    results = client.search(**search_params)
    jobs_results = results["jobs_results"]
    return jobs_results

preferred_role = 'AI Engineer'
jobs_results = scrape_google_jobs(query=preferred_role)