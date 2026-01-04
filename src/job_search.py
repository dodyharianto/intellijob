import pandas as pd
import serpapi
from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import List
from src.schemas import JobResult

load_dotenv()
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY') 

client = OpenAI()

def get_refined_search_query(user_query: str) -> str:
    system_prompt = """
    You are an expert in extracting interpreting the preferred job position/role based on user input.
    Only output a clear job title to be used for Google search.
    """

    response = client.responses.create(
        model='gpt-4o-mini',
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
    jobs_results = results.get('jobs_results')

    clean_jobs = []
    for job in jobs_results:
        clean_job = JobResult(
            title=job['title'],
            company=job['company_name'],
            location=job['location'],
            link=job['share_link'],
            description=job['description'],
            salary=job['detected_extensions'].get('salary'),
            posted_at=job['detected_extensions'].get('posted_at')
        )
        clean_jobs.append(clean_job)

    return clean_jobs