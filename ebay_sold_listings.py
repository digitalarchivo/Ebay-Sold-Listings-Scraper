import streamlit as st
from bs4 import BeautifulSoup
import requests

# Function to scrape eBay sold listings
def scrape_ebay_sold_listings(search_item):
    search_item = search_item.split(" ")
    search_item = "+".join(search_item)

    price_list = []

    # The range of pages starting at page 1 and ending at page 15
    for i in range(1, 16):
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_item}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={i}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        page = doc.find(class_="srp-results srp-list clearfix")

        listings = page.find_all("li", class_="s-item s-item__pl-on-bottom")

        for item in listings:
            title = item.find(class_="s-item__title").text
            price = item.find(class_="s-item__price").text
            date = item.find(class_="POSITIVE").string
            link = item.find(class_="s-item__link")['href'].split("?")[0]

            st.write(f"Title: {title}")
            st.write(f"Price: {price}")
            st.write(f"Date: {date}")
            st.write(f"Link: {link}")
            st.write("---")

            if price is not None:
                price = price.replace("$", "")
                if 'to' in price:
                    price = sum([float(num) for num in price.split() if num != 'to']) / 2
                    price = round(price, 2)
                if float(price) < 500:
                    price_list.append(float(price))

    price_list = list(set(price_list))

    if price_list:
        st.write(f"Highest Price: {max(price_list)}")
        st.write(f"Lowest Price: {min(price_list)}")
        st.write(f"Average Price: {round(sum(price_list) / len(price_list), 2)}")
    else:
        st.write("No items found matching the criteria.")

# Streamlit App
def main():
    st.title("eBay Sold Listings Scraper")

    search_item = st.text_input("Enter the eBay item:")
    if st.button("Scrape"):
        if search_item:
            st.write("Scraping eBay sold listings...")
            scrape_ebay_sold_listings(search_item)
        else:
            st.write("Please enter a search item.")

if __name__ == "__main__":
    main()
