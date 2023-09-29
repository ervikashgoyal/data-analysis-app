import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to clean text and numeric data by removing special characters, retaining dots
def clean_data(text):
    # Remove special characters and keep alphanumeric characters, spaces, and dots
    return re.sub(r'[^A-Za-z0-9\s.]+', '', text)

# Function to extract only numeric values from a text
def extract_numeric(text):
    # Use regular expressions to extract numeric values
    numeric_values = re.findall(r'\d+\.*\d*', text)
    if numeric_values:
        return numeric_values[0]
    return "N/A"

# Streamlit UI
st.title("Flipkart Product Scraper")
st.header("Developed by Vikash Goyal")
st.write("LinkedIn Profile: [Vikash Goyal](https://www.linkedin.com/in/vikash-goyal-20692924b)")
st.write("Fiverr Profile: [Vikash Goyal on Fiverr](https://www.fiverr.com/ervikashgoyal/expert-data-analyst-data-scientist-and-machine-learning-specialist-for-hire)")

# Input fields
st.subheader("Product Search")
search_query = st.text_input("Enter the product you want to search for:")

st.subheader("Scraping Settings")
max_page = st.slider("Select the maximum page number to scrape", 1, 50, 5)

if st.button("Scrape Data"):
    # Function to scrape product data from a Flipkart search page
    def scrape_flipkart_data(search_query, max_page):
        data = []  # Create an empty list to store the data

        for page_no in range(1, max_page + 1):
            url = f"https://www.flipkart.com/search?q={search_query}&page={page_no}"

            # Send an HTTP GET request to the URL
            response = requests.get(url)

            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, 'html.parser')

                product_cards = soup.find_all("div", class_="_1AtVbE")

                for card in product_cards:
                    product_name_element = card.find("div", class_="_4rR01T")
                    product_description_element = card.find("li", class_="rgWa7D")
                    product_price_element = card.find("div", class_="_30jeq3")
                    star_rating_element = card.find("div", class_="_3LWZlK")
                    image_element = card.find("img", class_="_396cs4")

                    # Original Price and Discount information
                    original_price_element = card.find("div", class_="_3I9_wc")
                    discount_element = card.find("div", class_="_3Ay6Sb")

                    # Check if the elements were found before accessing their 'text' attribute
                    product_name = product_name_element.text if product_name_element else "N/A"
                    product_description = product_description_element.text if product_description_element else "N/A"
                    product_price = clean_data(product_price_element.text) if product_price_element else "N/A"
                    star_rating = clean_data(star_rating_element.text) if star_rating_element else "N/A"
                    image_url = image_element['src'] if image_element and 'src' in image_element.attrs else "N/A"

                    original_price = clean_data(original_price_element.text) if original_price_element else "N/A"
                    discount = extract_numeric(clean_data(discount_element.text)) if discount_element else "N/A"

                    # Append the data to the list
                    data.append([product_name, product_description, original_price, discount, product_price, image_url])

        # Create a DataFrame from the list
        df = pd.DataFrame(data, columns=["Product Name", "Product Description", "Original Price", "Discount", "Product Price", "Image Link"])
        return df

    result_df = scrape_flipkart_data(search_query, max_page)

    # Filter rows where 'Product Name' is not 'N/A'
    result_df = result_df[result_df["Product Name"] != "N/A"]

    # Display the DataFrame
    st.dataframe(result_df)

    # Provide a link to download the DataFrame as an Excel file
    st.markdown(
        f"[:arrow_down: Download the data as Excel](data:text/csv;base64,{result_df.to_csv(index=False).encode().hex()})",
        unsafe_allow_html=True,
    )

# Usage instructions
st.subheader("How to Use This Web App")
st.write(
    "1. Enter the product you want to search for in the 'Product Search' input field."
    "\n2. Adjust the 'Select the maximum page number to scrape' slider to choose the number of pages you want to scrape (up to 50)."
    "\n3. Click the 'Scrape Data' button to start the scraping process."
    "\n4. The scraped data, including product names, descriptions, prices, discounts, original prices, and image links, will be displayed in the table."
    "\n5. You can download the scraped data as an Excel file by clicking the download link at the bottom of the table."
)
