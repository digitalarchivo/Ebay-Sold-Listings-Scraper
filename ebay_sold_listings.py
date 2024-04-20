import streamlit as st
from itertools import product
from bs4 import BeautifulSoup
import requests

# Function to generate search queries based on input data
def generate_search_queries(brand, sport, year, series, player_name):
    # Remove empty strings from input data
    inputs = [brand, sport, year, series, player_name]
    inputs = [inp.strip() for inp in inputs if inp.strip()]

    # Generate all possible combinations of input data
    combinations = list(product(*inputs))

    # Generate search queries for each combination
    search_queries = []
    for combo in combinations:
        query = " ".join(combo)
        search_queries.append(query)

    return search_queries

# Function to scrape eBay sold listings
def scrape_ebay_sold_listings(search_query):
    search_query = search_query.split(" ")
    search_query = "+".join(search_query)

    price_by_month = {}

    # The range of pages starting at page 1 and ending at page 15
    for i in range(1, 16):
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={i}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        page = doc.find(class_="srp-results srp-list clearfix")

        listings = page.find_all("li", class_="s-item s-item__pl-on-bottom")

        for item in listings:
            price = item.find(class_="s-item__price").text
            date = item.find(class_="POSITIVE").string

            # Extract month and year from the date string
            month_year = date.split(' ')[0]
            year = date.split(' ')[-1]
            month_year = f"{month_year}-{year}"

            # Append price to the corresponding month and year
            if month_year in price_by_month:
                price_by_month[month_year].append(price)
            else:
                price_by_month[month_year] = [price]

    return price_by_month

# Streamlit App
def main():
    st.title("eBay Sold Listings Scraper")

    # Input boxes for specific information
    brand = st.text_input("Brand (e.g., McFarlane):")
    sport = st.text_input("Sport (e.g., NBA, NFL, NHL, MLB):")
    year = st.text_input("Year (e.g., 2001 to 2009):")
    series = st.text_input("Series (e.g., 1-23):")
    player_name = st.text_input("Player Name:")

    if st.button("Scrape Sold Listings"):
        # Generate search queries based on input data
        search_queries = generate_search_queries(brand, sport, year, series, player_name)
        
        if search_queries:
            for query in search_queries:
                st.write(f"Scraping eBay sold listings for: {query}")
                price_by_month = scrape_ebay_sold_listings(query)
                if price_by_month:
                    for month_year, prices in price_by_month.items():
                        st.write(f"Month-Year: {month_year}")
                        st.write("Prices:")
                        for price in prices:
                            st.write(price)
                        st.write("---")
                else:
                    st.write("No items found matching the criteria.")
        else:
            st.write("Please fill in at least one input box.")

if __name__ == "__main__":
    main()
