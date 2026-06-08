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
        # Added countryCode for India (IN)
        run_input = {
            "queries": keyword, 
            "resultsPerPage": 20, 
            "maxPagesPerQuery": 1,
            "countryCode": "IN", 
            "languageCode": "en"
        }
        
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)
        dataset_client = client.dataset(run.default_dataset_id)
        results = dataset_client.list_items().items
        
        if not results:
            return {"rank": "No Results Found by Scraper"}

        organic_results = results[0].get("organicResults", [])
        
        # DEBUG: Print found URLs to Vercel Logs so you can see what is happening
        found_urls = [item.get("url", "") for item in organic_results]
        print(f"DEBUG: Scraper found these URLs: {found_urls}")

        # Improved matching: Check if domain exists in URL without being picky about 'www'
        target_domain = "ultimatesmiledesign.com"
        
        for pos, item in enumerate(organic_results, 1):
            url = item.get("url", "").lower()
            if target_domain in url:
                return {"rank": pos}
        
        return {"rank": "Not in Top 20 (Found: " + str(found_urls[:3]) + " )"}
        
    except Exception as e:
        return {"rank": f"Error: {str(e)}"}
