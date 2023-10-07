from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from requests.exceptions import ConnectTimeout
import time

max_retries = 3
retries = 0

while retries < max_retries:
    try:
        response = requests.get('https://www.flipkart.com')
        # Process the response here
        break  # Break the loop if the request is successful
    except ConnectTimeout:
        print("Request timed out. Retrying...")
        retries += 1
        time.sleep(5)  # Wait for a few seconds before retrying


# Function to extract Product Title
def scrape_flipkart(product_name):
    def get_title(soup):

        try:
            # Outer Tag Object
            title = soup.find("span", attrs={"class":'B_NuCI'})
            
            # Inner NavigatableString Object
            title_value = title.text

            # Title as a string value
            title_string = title_value.strip()

        except AttributeError:
            title_string = ""

        return title_string

    # Function to extract Product Price
    def get_price(soup):

        try:
            price = soup.find("div", attrs={'class':'_30jeq3 _16Jk6d'}).string.strip()

        except AttributeError:

            try:
                # If there is some deal price
                price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

            except:
                price = ""

        return price

    # Function to extract Product Rating
    def get_rating(soup):

        try:
            rating = soup.find("div",attrs={"class":'_3LWZlK'}).text
        
        except AttributeError:
            try:
                rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
            except:
                rating = ""

        return rating

    # Function to extract Number of User Reviews
    def get_review_count(soup):
        try:
            review_count = soup.find("span",attrs={"class":'_2_R_DZ'}).text.split(" ")[0]

        except AttributeError:
            review_count = ""

        return review_count

    # Function to extract Seller Name
    def get_bought(soup):
        try:
            seller_name = soup.find("div",attrs={"id":'sellerName'}).text.strip()[:-3]

        except AttributeError:
            seller_name = ""

        return seller_name

    # Function to extract Highlights of the Product
    def get_highlights(soup):
        try:
            highlights=list(soup.find("div",attrs={"class":'_2418kt'}).find_all("li",attrs={"class":"_21Ahn-"}))
            high_list=""
            for i in highlights:
                high_list+=i.text.strip()+", "
            high_list1=high_list[:-3]

        except AttributeError:
            high_list1 = ""

        return high_list1

    # add your user agent 
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    
    product_name=product_name.replace(" ","+")
    URL = f"https://www.flipkart.com/search?q={product_name}"
    
    print(URL)

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
    print(webpage)
    

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'s1Q9rs'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"Name of the Product":[], "Price":[], "Star Ratings":[], "No. of Ratings":[],"Seller Name":[],"Highlights":[]}
    
    # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get("https://www.flipkart.com"+link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
        # Function calls to display all necessary product information
        d['Name of the Product'].append(get_title(new_soup))
        d['Price'].append(get_price(new_soup))
        d['Star Ratings'].append(get_rating(new_soup))
        reviu=get_review_count(new_soup)
        if('(' in reviu):
            reviu=reviu[1:-1]
        d['No. of Ratings'].append(reviu)
        d['Seller Name'].append(get_bought(new_soup))
        d['Highlights'].append(get_highlights(new_soup))
        
    return d
        