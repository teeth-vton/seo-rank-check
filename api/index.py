from apify_client import ApifyClient

import os
client = ApifyClient(os.getenv("APIFY_TOKEN"))

def get_rank_from_apify(keyword):
    # This prepares the actor call to the Google Search Scraper
    run_input = {
        "queries": keyword,
        "resultsPerPage": 20, # We only need top 20
        "maxPagesPerQuery": 1
    }
    
    # Run the actor and wait for it to finish
    run = client.actor("apify/google-search-scraper").call(run_input=run_input)
    
    # Fetch the results
    dataset = client.dataset(run["defaultDatasetId"])
    results = dataset.list_items().items[0]
    
    # Find ultimate smile designing
    for pos, item in enumerate(results.get("organicResults", []), 1):
        if "ultimatesmiledesign.com" in item["url"]:
            return pos
    return "Not in Top 20"
