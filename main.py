from scrapers.county_scraper import scrape_all_counties
from enrichment.skip_tracer import enrich_lead
from database import init_db, save_lead
from export import export_to_csv
import os

def main():
    print("=== Real Estate Pre-Foreclosure Lead Pipeline ===")
    
    # Ensure working directory is the script's directory for relative paths
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Initialize Database
    init_db()
    
    # 2. Scrape Public Records from all 3 counties
    raw_leads = scrape_all_counties()
    
    new_leads_added = 0
    
    # 3. Enrich & Save
    print("Processing and enriching leads...")
    for lead in raw_leads:
        enriched_lead = enrich_lead(lead)
        was_saved = save_lead(enriched_lead)
        
        if was_saved:
            new_leads_added += 1
            print(f"  [+] Saved new lead: {enriched_lead['owner_name']}")
        else:
            print(f"  [-] Skipped duplicate: {enriched_lead['owner_name']}")
            
    print(f"Finished processing. {new_leads_added} new leads added to database.")
    
    # 4. Export to CSV for buyers
    if new_leads_added > 0:
        export_to_csv()

if __name__ == "__main__":
    main()
