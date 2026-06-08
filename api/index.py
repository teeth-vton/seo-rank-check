from fastapi import FastAPI
from apify_client import ApifyClient
import os

app = FastAPI()

@app.get("/api/index")
async def get_rank(keyword: str):
    token = os.getenv("APIFY_TOKEN")
    if not token:
        return {"rank": "Error: Missing Token"}
    
    try:
        client = ApifyClient(token)
        # Use lowercase 'in' for India
        run_input = {
            "queries": keyword, 
            "resultsPerPage": 20, 
            "maxPagesPerQuery": 1,
            "countryCode": "in", 
            "languageCode": "en"
        }
        
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)
        dataset_client = client.dataset(run.default_dataset_id)
        results = dataset_client.list_items().items
        
        if not results:
            return {"rank": "No Results Found"}

        organic_results = results[0].get("organicResults", [])
        
        # LOGGING: This will appear in your Vercel Function Logs
        print(f"Scraper data for '{keyword}': Found {len(organic_results)} results.")
        
        # Check matching
        target_domain = "ultimatesmiledesign.com"
        for pos, item in enumerate(organic_results, 1):
            url = item.get("url", "").lower()
            if target_domain in url:
                return {"rank": pos}
        
        return {"rank": "Not in Top 20"}
        
    except Exception as e:
        # This will show the actual API error in your browser if something breaks
        return {"rank": f"Error: {str(e)}"}
