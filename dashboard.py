import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Pre-Foreclosure Leads", page_icon="🏠", layout="wide")

DB_NAME = os.path.join(os.path.dirname(__file__), "leads.db")

@st.cache_data(ttl=60)
def load_data():
    if not os.path.exists(DB_NAME):
        return pd.DataFrame()
        
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT id, owner_name, property_address, property_value, delinquent_amount, phone_1, email FROM leads"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("🏠 Real Estate Pre-Foreclosure Leads")
st.markdown("View and filter your enriched tax-delinquent properties.")

df = load_data()

if df.empty:
    st.warning("No leads found in the database yet. Run `python main.py` to scrape and enrich leads!")
else:
    # Metrics
    total_leads = len(df)
    leads_with_phones = len(df[~df['phone_1'].isin(['None found', 'Not found', 'API Error', 'Error'])])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads", total_leads)
    col2.metric("Leads with Phone Numbers", leads_with_phones)
    col3.metric("Contact Match Rate", f"{(leads_with_phones/total_leads)*100:.1f}%")
    
    st.divider()
    
    # 1. Why are there only a few addresses?
    st.info("**Why are there only a few addresses?** Currently, the Playwright Scraper is running in *Prototype Mode*. It deliberately fetches a small handful of properties from each county to prove that it can successfully bypass the government 403 firewalls. A full production run involves scraping hundreds of pages, which takes hours to execute.")
    
    # 2. Investor Playbook (What to do with the house)
    with st.expander("📖 Investor Playbook: What do I do with these houses?"):
        st.markdown("""
        **These properties are behind on their taxes. The owners are highly motivated to sell before the county forecloses on them. Here is your process:**
        
        1. **Call them:** Use the phone numbers provided by the Skip Tracer API to call or text the owner.
        2. **Make a cash offer:** Offer to buy the house for cash, slightly below market value, so they can pay off their tax debt and walk away with money.
        3. **Wholesale it (No money needed):** Once they agree to sell, sign a Purchase Agreement. Then, find a local house flipper and "assign" the contract to them for a $5,000 - $10,000 finder's fee.
        4. **Flip it:** If you have capital, buy the house yourself, renovate it, and sell it on the open market.
        """)

    st.divider()
    
    # Search and Filter
    search_term = st.text_input("🔍 Search by Owner Name or Address:", "")
    
    # Create the Map Link column
    import urllib.parse
    df['Map Link'] = df['property_address'].apply(lambda x: f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(x)}")
    
    if search_term:
        mask = df['owner_name'].str.contains(search_term, case=False, na=False) | \
               df['property_address'].str.contains(search_term, case=False, na=False)
        display_df = df[mask]
    else:
        display_df = df
        
    st.dataframe(
        display_df,
        column_config={
            "id": st.column_config.NumberColumn("ID", format="%d"),
            "owner_name": "Owner Name",
            "property_address": "Property Address",
            "Map Link": st.column_config.LinkColumn(
                "View on Map",
                display_text="Open Google Maps 🗺️"
            ),
            "property_value": "Property Value",
            "delinquent_amount": "Delinquent Amount",
            "phone_1": "Phone Number",
            "email": "Email Address"
        },
        hide_index=True,
        use_container_width=True
    )
