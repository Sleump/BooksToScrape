import csv
from bs4 import BeautifulSoup as bs, BeautifulSoup
import requests
from csv import writer

url = "https://books.toscrape.com/index.html"


def get_page(url_link):
    page = requests.get(url_link)
    status = page.status_code
    soup = BeautifulSoup(page.content, 'lxml')
    return [soup, status]



def get_links(soup):
    # get all book links
    links = []
    listings = soup.find_all(class_="product_pod")
    for listing in listings:
        suite_url = listing.find("h3").a.get("href")
        base_url = "https://books.toscrape.com/"
        full_url = base_url + suite_url
        links.append(full_url)
    return links

soup, status = get_page(url)
links = get_links(soup)
print(links)
print(len(links))