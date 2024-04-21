import streamlit as st
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
from datetime import datetime

# Function to scrape eBay sold listings
def scrape_ebay_sold_listings(search_query):
    search_query = search_query.split(" ")
    search_query = "+".join(search_query)

    price_by_month = defaultdict(list)

    # The range of pages starting at page 1 and ending at page 15
    for i in range(1, 16):
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={i}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        page = doc.find(class_="srp-results srp-list clearfix")

        listings = page.find_all("li", class_="s-item s-item__pl-on-bottom")

        for item in listings:
            title = item.find(class_="s-item__title").text
            price = item.find(class_="s-item__price").text
            date_str = item.find(class_="POSITIVE").string

            # Parse date string into datetime object
            try:
                date = datetime.strptime(date_str, "%b-%d %H:%M")
            except ValueError:
                # Some listings might have different date formats, ignore them
                continue

            # Group prices by month and year
            month_year = date.strftime("%b-%Y")
            price_by_month[month_year].append(price)

    for month_year, prices in price_by_month.items():
        st.write(f"Month-Year: {month_year}")
        st.write("Prices:")
        for price in prices:
            st.write(price)
        st.write("---")

# Streamlit App
def main():
    st.title("eBay Sold Listings Scraper")

    # Dropdown selectors for specific information
    brand_options = ["McFarlane", "Kenner SLU"]
    brand = st.selectbox("Brand", options=brand_options)

    sport_options = ["NBA", "NFL", "NHL", "MLB"]
    sport = st.selectbox("Sport", options=sport_options)

    year_options = [str(year) for year in range(1988, 2021)]
    year = st.selectbox("Year", options=year_options)

    series_options = [str(series) for series in range(1, 24)]
    series = st.selectbox("Series", options=series_options)

    # Search box for custom search
    custom_search = st.text_input("Custom Search")

    # Construct search query
    search_query = " ".join([brand, sport, year, series, custom_search])

    if st.button("Scrape Sold Listings"):
        if search_query.strip():
            st.write("Scraping eBay sold listings...")
            scrape_ebay_sold_listings(search_query)
        else:
            st.write("Please fill in at least one input box.")

    # Embed Airtable database
    st.write("## Embedded Airtable Database")
    st.markdown("""
        <iframe 
            class="airtable-embed" 
            src="https://airtable.com/embed/appGmHhILJWl81a00/shrlFSwDvbDWsjWcb?backgroundColor=green&viewControls=on" 
            frameborder="0" 
            onmousewheel="" 
            width="100%" 
            height="533" 
            style="background: transparent; border: 1px solid #ccc;">
        </iframe>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
