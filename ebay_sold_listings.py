import streamlit as st
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
from datetime import datetime
import pandas as pd
<<<<<<< Updated upstream
=======
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
>>>>>>> Stashed changes

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

    return price_by_month

# Function to save data to GitHub Gist
def save_to_github_gist(data, access_token):
    gist_url = "https://api.github.com/gists"
    headers = {"Authorization": f"token {access_token}"}
    files = {"data.csv": {"content": data.to_csv(index=False)}}
    payload = {"description": "eBay Sold Listings Data", "public": True, "files": files}

    response = requests.post(gist_url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()["html_url"]
    else:
        return None

# Streamlit App
def main():
    # Apply background image
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url("https://i.ibb.co/8mTYfNb/background.jpg") no-repeat center center;
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("eBay Sold Listings Scraper")

    # Dropdown selectors for specific information
    brand_options = ["McFarlane", "Kenner SLU"]
    brand = st.selectbox("Brand", options=brand_options)

    sport_options = ["NBA", "NFL", "NHL", "MLB"]
    sport = st.selectbox("Sport", options=sport_options)
<<<<<<< Updated upstream

    year_options = [str(year) for year in range(1988, 2021)]
    year = st.selectbox("Year", options=year_options)

    series_options = [str(series) for series in range(1, 24)]
    series = st.selectbox("Series", options=series_options)
=======

    year_options = [str(year) for year in range(1988, 2021)]
    year = st.selectbox("Year", options=year_options)
>>>>>>> Stashed changes

    player_name = st.text_input("Player Name")

    # Construct search query
    search_query = " ".join([brand, sport, year, series, player_name])

    custom_search = st.text_input("Custom Search")

    if st.button("Search"):
        if custom_search.strip():
            search_query = custom_search.strip()

        if search_query.strip():
            st.write(f"Scraping eBay sold listings for: {search_query}...")
            results = scrape_ebay_sold_listings(search_query)
            st.write("## eBay Sold Listings:")
            for month_year, prices in results.items():
                st.write(f"Month-Year: {month_year}")
                st.write("Prices:")
                for price in prices:
                    st.write(price)
                st.write("---")
            
            # Convert results to DataFrame
            df = pd.DataFrame([(month_year, price) for month_year, prices in results.items() for price in prices], columns=["Month-Year", "Price"])
            
            # Save results to GitHub
<<<<<<< Updated upstream
            github_token = "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"
=======
            github_token = os.getenv("GITHUB_TOKEN")
>>>>>>> Stashed changes
            gist_url = save_to_github_gist(df, github_token)
            if gist_url:
                st.write("## Saving Results to GitHub:")
                st.write("Results saved to GitHub Gist successfully!")
                st.write("You can view the results at the following URL:")
                st.write(gist_url)
            else:
                st.write("Failed to save results to GitHub.")

        else:
            st.write("Please fill in at least one input box.")

if __name__ == "__main__":
    main()
