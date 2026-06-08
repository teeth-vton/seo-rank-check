from fastapi import FastAPI
from apify_client import ApifyClient
import os

app = FastAPI()

# Ensure APIFY_TOKEN is set in Vercel Environment Variables
client = ApifyClient(os.getenv("APIFY_TOKEN"))

@app.get("/api/get-rank")
async def get_rank(keyword: str):
    try:
        run_input = {"queries": keyword, "resultsPerPage": 20, "maxPagesPerQuery": 1}
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)
        dataset = client.dataset(run["defaultDatasetId"])
        results = dataset.list_items().items
        
        if not results:
            return {"rank": "No results"}

        for pos, item in enumerate(results[0].get("organicResults", []), 1):
            if "ultimatesmiledesign.com" in item.get("url", ""):
                return {"rank": pos}
        return {"rank": "Not in Top 20"}
    except Exception as e:
        return {"rank": f"Error: {str(e)}"}
