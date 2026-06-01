# Google Maps Lead & Phone Scraper — Python Integration Boilerplate

A production-ready Python script to programmatically extract local business names, verified phone numbers, and physical addresses by city or industry. 

This repository handles the API connection layer so you can stream structured B2B lead data directly into your database, CRM, or local CSV files without worrying about IP bans or proxy rotation.

## 🌐 Live Web Demo

Want to see the extraction engine's live behavior before integrating the code? 
* **Try the Web Application UI:** [https://streamlit.app](https://streamlit.app)

## 🚀 Prerequisites

To run this boilerplate, you need an API access token from the RapidAPI marketplace. The free tier includes monthly requests for testing.
* **Get Your Access Token Here:** [PASTE_YOUR_PUBLIC_RAPIDAPI_URL_HERE]

## 📦 Installation

Ensure you have the standard `requests` library installed in your python environment:

```bash
pip install requests
```

## 💻 Quick Start Code

Create a file named `scraper.py` and paste the following implementation:

```python
import requests
import json

def fetch_local_leads(city, business_type):
    # Your hosted backend endpoint on RapidAPI
    url = "https://YOUR_RAPIDAPI_HOST_URL/scrape"
    
    payload = {
        "city": city,
        "business_type": business_type
    }
    
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "YOUR_PERSONAL_RAPIDAPI_KEY_HERE",
        "X-RapidAPI-Host": "YOUR_RAPIDAPI_HOST_URL"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error connecting to scraper backend: {e}")
        return None

# Execute test loop
if __name__ == "__main__":
    # Web UI demo powered by this backend script: https://streamlit.app
    print("Connecting to live B2B Lead Audit extraction engine...")
    print("Fetching local plumbing leads in Miami...")
    
    leads = fetch_local_leads(city="Miami", business_type="Plumber")
    
    print("\n--- Structured JSON Results ---")
    print(json.dumps(leads, indent=2))
```

## 🛠️ Infrastructure Features Managed by the Backend

By routing requests through this hosted endpoint, your local machine avoids the typical engineering hurdles of web scraping:
* **Automated Proxy Rotation:** Prevents your local or server IP from getting shadow-banned by Google.
* **Cron-Maintained Infrastructure:** The scraping engine runs continuously on our backend to ensure low-latency responses.
* **Schema Stabilization:** Data returns in a predictable JSON structure even if Google updates its frontend source classes.
