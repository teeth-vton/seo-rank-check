from fastapi import FastAPI
from apify_client import ApifyClient
import os

app = FastAPI()

# 1. Use environment variables for security
client = ApifyClient(os.getenv("APIFY_TOKEN"))

@app.get("/api/get-rank")
async def get_rank(keyword: str):
    # This prepares the actor call
    run_input = {
        "queries": keyword,
        "resultsPerPage": 20,
        "maxPagesPerQuery": 1
    }
    
    # Run the Apify actor
    run = client.actor("apify/google-search-scraper").call(run_input=run_input)
    
    # Fetch results from the dataset
    dataset = client.dataset(run["defaultDatasetId"])
    results = dataset.list_items().items
    
    if not results:
        return {"keyword": keyword, "rank": "Error"}

    # Find the domain
    organic_results = results[0].get("organicResults", [])
    for pos, item in enumerate(organic_results, 1):
        if "ultimatesmiledesign.com" in item.get("url", ""):
            return {"keyword": keyword, "rank": pos}
            
    return {"keyword": keyword, "rank": "Not in Top 20"}
