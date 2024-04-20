import streamlit as st
from itertools import product

# Function to generate possible search queries
def generate_queries(brand, sport, year, series, player_name):
    # Remove empty strings from input lists
    brand = [item.strip() for item in brand if item.strip()]
    sport = [item.strip() for item in sport if item.strip()]
    year = [item.strip() for item in year if item.strip()]
    series = [item.strip() for item in series if item.strip()]
    player_name = [item.strip() for item in player_name if item.strip()]

    # Generate combinations of input values
    combinations = list(product(brand, sport, year, series, player_name))
    queries = []

    # Create search queries
    for combo in combinations:
        query = " ".join(combo)
        queries.append(query)

    return queries

# Streamlit App
def main():
    st.title("eBay Sold Listings Scraper")

    # Input boxes for specific information
    brand = st.text_input("Brand (e.g., McFarlane):")
    sport = st.text_input("Sport (e.g., NBA, NFL, NHL, MLB):")
    year = st.text_input("Year (e.g., 2001 to 2009):")
    series = st.text_input("Series (e.g., 1-23):")
    player_name = st.text_input("Player Name:")

    if st.button("Generate Queries"):
        # Check if any input is empty
        if not all([brand, sport, year, series, player_name]):
            st.write("Please fill in at least one input box.")
            return

        st.write("Generating possible search queries...")
        queries = generate_queries(brand.split(), sport.split(), year.split(), series.split(), player_name.split())

        st.write("Possible Search Queries:")
        for query in queries:
            st.write(query)

if name == "main":
    main()import streamlit as st
from itertools import product

# Function to generate possible search queries
def generate_queries(brand, sport, year, series, player_name):
    # Remove empty strings from input lists
    brand = [item.strip() for item in brand if item.strip()]
    sport = [item.strip() for item in sport if item.strip()]
    year = [item.strip() for item in year if item.strip()]
    series = [item.strip() for item in series if item.strip()]
    player_name = [item.strip() for item in player_name if item.strip()]

    # Generate combinations of input values
    combinations = list(product(brand, sport, year, series, player_name))
    queries = []

    # Create search queries
    for combo in combinations:
        query = " ".join(combo)
        queries.append(query)

    return queries

# Streamlit App
def main():
    st.title("eBay Sold Listings Scraper")

    # Input boxes for specific information
    brand = st.text_input("Brand (e.g., McFarlane):")
    sport = st.text_input("Sport (e.g., NBA, NFL, NHL, MLB):")
    year = st.text_input("Year (e.g., 2001 to 2009):")
    series = st.text_input("Series (e.g., 1-23):")
    player_name = st.text_input("Player Name:")

    if st.button("Generate Queries"):
        # Check if any input is empty
        if not all([brand, sport, year, series, player_name]):
            st.write("Please fill in at least one input box.")
            return

        st.write("Generating possible search queries...")
        queries = generate_queries(brand.split(), sport.split(), year.split(), series.split(), player_name.split())

        st.write("Possible Search Queries:")
        for query in queries:
            st.write(query)

if name == "main":
    main()
