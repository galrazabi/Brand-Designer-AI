from serpapi import GoogleSearch
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
serp_key = os.getenv("SERP_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(message)s')

def get_google_image(company_name : str):
    logging.info("Contacting serpAPI")
    img_url = None

    try:
        input_search = company_name + " logo"
        params = {
        "q": f"{input_search}",
        "engine": "google_images",
        "ijn": "0",
        "api_key": serp_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        images_results = results.get("images_results", [])

        img_url = images_results[0]['thumbnail']
        
        logging.info("Contacted serpAPI successfully")
    except:
        logging.error("Error contacting serpAPI")
        
    return img_url


