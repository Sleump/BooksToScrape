# -*- coding: utf-8 -*-
import csv
import os
from bs4 import BeautifulSoup
import requests
from csv import writer

def remove_special_characters_from_title(title):
    return "".join(char for char in title if char.isalnum())

def create_category_folder(name):
    if not os.path.isdir(name):
        os.mkdir(name)

def extract_info(url):
    #get informations for a book
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Site non accessible")

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text()
    find_p_in_page = soup.find_all("p")
    description = find_p_in_page[3].text
    cells = soup.find_all('td')
    universal_product_code = cells[0].string
    price_excluding_tax = cells[2].string
    price_including_tax = cells[3].string
    number_available = cells[5].string
    mapping_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    review_rating = soup.find_all("p", class_="star-rating")[0].get("class")[1]
    rating_number = f"{mapping_rating[review_rating]} / 5"
    category = soup.find_all('li')[2].a.text
    article = soup.find('article')
    imgsrc = article.find("img").get("src")[6:]
    # Download and place an image in a folder
    url_base = "https://books.toscrape.com/"
    image_url = url_base + imgsrc
    img = requests.get(image_url)
    title_without_special_characters = remove_special_characters_from_title(title)
    file = open(f"{category}/{title_without_special_characters}.png", "wb")
    file.write(img.content)
    file.close()
    # Return data in a Dictionary
    book_details = {"title": title, "universal_product_code": universal_product_code, "url": url,
                    "PrixHT": price_excluding_tax, "PrixTTC": price_including_tax, "Stock": number_available,
                    "Description": description, "Categorie": category,
                    "Note": rating_number, "UrlImage": image_url, "book url": url}
    return book_details


#get categories names and links
url2 = 'https://books.toscrape.com/index.html'
page = requests.get(url2)
soup = BeautifulSoup(page.text, 'lxml')

categories = {}

# Je récupére l'endroit dans la page ou est la liste de catégorie
side_categories = soup.find("ul", class_="nav-list")

# Je récupère les balises li à l'intérieur de cette balise ul
puces = side_categories.find_all("li")[1:]
# Find all retourne une list de balise li

# Pour chaque balise li, je récupère le titre de la catégorie et le lien
for puce in puces:
    link = puce.find("a")
    name = link.get_text() # A verifier pour la correct syntaxe
    name = name.replace("\n", "")
    name = name.strip()
# Je stocke ma catégorie est lien dans un dictionnaire pour réutilisation plus tard
    categories[name] = link.get("href")


links = []

def write_csv(books, category_name):
    #write on a csv file the informations about the books
    with open(f"{category_name}/books.csv", 'w', encoding="utf-8") as csvfile:
        fieldnames = ['title', 'universal_product_code', 'url', 'PrixHT', 'PrixTTC', 'Stock', 'Description',
                      'Categorie', 'Note', 'UrlImage']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for book in books:
            writer.writerow(book)
books = []
for name, link in categories.items():
    create_category_folder(name)
    print(name, link)
    url2 = link
    pg = 1
    category_new = link.replace("index.html", "")
    base_url = "https://books.toscrape.com/"
    category_full = base_url + category_new
    response = requests.get(category_full)
    soup = BeautifulSoup(response.content, 'lxml')
    pages_category = soup.find('li', class_="current")
    #regarder ce qu'il y a dans pages_category
    articles = soup.find_all('article', class_="product_pod")
    for article in articles:
        relative_book_url = article.find("h3").a.get("href")[9:]
        base_url = "https://books.toscrape.com/catalogue/"
        book_link = base_url + relative_book_url
        book_details = extract_info(book_link)
        books.append(book_details)
    pages_category = soup.find('li', class_="current")
    if pages_category:
        pages_category = pages_category.text
        pages_category_soup = pages_category.split()
        pages_category_nombre = int(pages_category_soup[3])
        for pg in range(pages_category_nombre):
            pg += 1
            category_full = category_new + f"page-{pg}"
            response = requests.get(base_url + category_full)
            soup = BeautifulSoup(response.content, 'lxml')
            # obtenir l'url de chaque page de la catégorie + extraire les infos
            articles = soup.find_all('article', class_="product_pod")
            for article in articles:
                relative_book_url = article.find("h3").a.get("href")[9:]
                base_url = "https://books.toscrape.com/catalogue/"
                book_link = base_url + relative_book_url
                book_details = extract_info(book_link)
                books.append(book_details)
    else :
        print("Pas d'autre pages pour cette categorie " + f"{name}")


    write_csv(books, name)








