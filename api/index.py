from fastapi import FastAPI
from apify_client import ApifyClient
import os

app = FastAPI()

@app.get("/api/get-rank")
async def get_rank(keyword: str):
    token = os.getenv("APIFY_TOKEN")
    if not token:
        return {"rank": "Error: APIFY_TOKEN missing"}
    
    try:
        client = ApifyClient(token)
        
        # Run the actor
        run_input = {"queries": keyword, "resultsPerPage": 20, "maxPagesPerQuery": 1}
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)
        
        # Access attributes directly (Apify Python SDK uses attributes, not dict keys)
        dataset_id = run.default_dataset_id
        
        # Fetch results
        dataset_client = client.dataset(dataset_id)
        results = dataset_client.list_items().items
        
        if not results:
            return {"rank": "No results found"}

        # Search for domain
        organic_results = results[0].get("organicResults", [])
        for pos, item in enumerate(organic_results, 1):
            if "ultimatesmiledesign.com" in item.get("url", ""):
                return {"rank": pos}
        
        return {"rank": "Not in Top 20"}
    except Exception as e:
        return {"rank": f"Error: {str(e)}"}
