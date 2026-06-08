from fastapi import FastAPI
from apify_client import ApifyClient
import os

app = FastAPI()

@app.get("/api/get-rank")
async def get_rank(keyword: str):
    try:
        # Initialize client inside the route to ensure it catches the token
        token = os.getenv("APIFY_TOKEN")
        if not token:
            return {"error": "Token Missing"}
        
        client = ApifyClient(token)
        
        # Scraper logic
        run_input = {"queries": keyword, "resultsPerPage": 20, "maxPagesPerQuery": 1}
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)
        
        dataset = client.dataset(run["defaultDatasetId"])
        results = dataset.list_items().items
        
        if not results:
            return {"rank": "No results"}

        # Search for your domain
        organic_results = results[0].get("organicResults", [])
        for pos, item in enumerate(organic_results, 1):
            if "ultimatesmiledesign.com" in item.get("url", ""):
                return {"rank": pos}
        
        return {"rank": "Not in Top 20"}
        
    except Exception as e:
        return {"rank": f"Error: {str(e)}"}
