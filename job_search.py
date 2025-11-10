import pandas as pd
import serpapi
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY') 

client = OpenAI()

def get_refined_search_query(user_query: str):
    system_prompt = """
    You are an expert in extracting interpreting the preferred job position/role based on user input.
    Only output a clear job position to be used for Google search.
    """

    response = client.responses.create(
        model='gpt-5-nano',
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    )

    search_query = response.output_text
    return search_query

def scrape_google_jobs(query: str):
    refined_query = get_refined_search_query(query)
    print(f'Searching for: {refined_query}')
    search_params = {
        "engine": "google_jobs",
        "q": refined_query,
        "hl": "en",
        "location": "Singapore",
        "api_key": SERPAPI_API_KEY
    }

    results = serpapi.search(**search_params)
    jobs_results = results["jobs_results"]
    jobs_results_df = pd.DataFrame(jobs_results)
    return jobs_results_df