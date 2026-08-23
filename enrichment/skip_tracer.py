import os
import requests
import time

# User's provided API Key (Assuming PeopleDataLabs based on format)
PDL_API_KEY = "c00a58528a22fe15d0729e431e8a3f8eddc0f5469627365cc52a2621c40c7b48"

def enrich_lead(lead_data):
    """
    Takes a single lead dictionary and queries the PeopleDataLabs API
    to find phone numbers and email addresses.
    """
    print(f"Skip tracing {lead_data['owner_name']} via API...")
    
    enriched_data = lead_data.copy()
    
    # Setup PeopleDataLabs Enrichment API parameters
    url = "https://api.peopledatalabs.com/v5/person/enrich"
    headers = {
        "X-Api-Key": PDL_API_KEY,
        "Content-Type": "application/json"
    }
    
    # We pass the name and the property address to find a match
    params = {
        "name": lead_data['owner_name'],
        "location": lead_data['property_address']
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            
            # Extract the first phone number if available
            phones = data.get('phone_numbers', [])
            enriched_data['phone_1'] = phones[0] if phones else "Not found"
            
            # Extract the first email if available
            emails = data.get('emails', [])
            enriched_data['email'] = emails[0]['address'] if emails and isinstance(emails[0], dict) else (emails[0] if emails else "Not found")
        elif response.status_code == 404:
            print(f"  [-] No match found for {lead_data['owner_name']}")
            enriched_data['phone_1'] = "Not found"
            enriched_data['email'] = "Not found"
        else:
            print(f"  [!] API Error: {response.status_code} - {response.text}")
            enriched_data['phone_1'] = "API Error"
            enriched_data['email'] = "API Error"
            
    except Exception as e:
        print(f"  [!] Connection Error: {e}")
        enriched_data['phone_1'] = "Error"
        enriched_data['email'] = "Error"
        
    time.sleep(0.5) # Slight delay to respect API rate limits
    return enriched_data
