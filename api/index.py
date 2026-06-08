from fastapi import FastAPI
from apify_client import ApifyClient
import os

app = FastAPI()

@app.get("/api/index")
async def get_rank(keyword: str):
    token = os.getenv("APIFY_TOKEN")
    if not token:
        return {"rank": "Error", "url": "Missing Token"}
    
    try:
        client = ApifyClient(token)
        run_input = {
            "queries": keyword, 
            "resultsPerPage": 20, 
            "maxPagesPerQuery": 1,
            "countryCode": "in", 
            "languageCode": "en"
        }
        
        # Run scraper
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)
        dataset_client = client.dataset(run.default_dataset_id)
        results = dataset_client.list_items().items
        
        if not results:
            return {"rank": "No Results", "url": "-"}

        organic_results = results[0].get("organicResults", [])
        
        # DEBUG: This print will help you see what the scraper actually sees 
        # Check your Vercel Function Logs to verify this!
        print(f"Scraper found {len(organic_results)} results for '{keyword}'")

        target_domain = "ultimatesmiledesign.com"
        for pos, item in enumerate(organic_results, 1):
            url = item.get("url", "").lower()
            if target_domain in url:
                # Return BOTH rank and the specific URL found
                return {"rank": pos, "url": item.get("url")}
        
        return {"rank": "Not in Top 20", "url": "-"}
        
    except Exception as e:
        return {"rank": "Error", "url": str(e)}
