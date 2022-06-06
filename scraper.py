import csv

from bs4 import BeautifulSoup
import requests
from csv import writer
import logging

# coding: utf-8
from main import links


def extract_info(link):
    #print 'Veuillez entrer le lien du livre entre guillemets'
    # url = input()
    url= links
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Site non accessible")

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text()
    table = soup.find("table", { "class" : "table table-striped"})
    description = soup.find('id_="product_description"')
    cells = soup.find_all('td')
    universal_product_code = cells[0].string
    price_excluding_tax = cells[2].string
    price_including_tax = cells[3].string
    number_available = cells[5].string
    mapping_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    review_rating = soup.find_all("p", class_="star-rating")[0].get("class")[1]
    mapping_rating[review_rating]
    rating_number = f"{review_rating} / 5"
    product_page_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    category = soup.find_all('li')[2].a.text
    article = soup.find('article')
    imgsrc = article.find("img").get("src")[6:]
    url_base = "https://books.toscrape.com/"
    image_url = url_base + imgsrc
    img_data = requests.get(image_url).content
    #with open('title.jpg', 'wb') as handler:
        #handler.write(img_data)








