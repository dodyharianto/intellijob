from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SERPAPI_KEY = os.getenv('SERPAPI_KEY') 

def scrape_google_jobs(query):
    params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs_results = results["jobs_results"]
    return job_results

preferred_role = 'AI Engineer'
job_results = scrape_google_jobs(query=preferred_role)