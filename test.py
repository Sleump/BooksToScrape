import csv
from bs4 import BeautifulSoup as bs, BeautifulSoup
import requests
from csv import writer



url = "https://books.toscrape.com/index.html"


def get_page(url):
    page = requests.get(url)
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


def extract_info(links:list):
    """ Extract info for book"""
    all_books = []
    for link in links:
        """Définir un nouveau point de départ"""
        book_soup = get_page(link)


        title = book_soup.find('h1').get_text()
        table = book_soup.find("table", {"class": "table table-striped"})
        description = book_soup.find('id_="product_description"')
        cells = book_soup.find_all('td')
        universal_product_code = cells[0].string
        price_excluding_tax = cells[2].string
        price_including_tax = cells[3].string
        number_available = cells[5].string
        mapping_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        review_rating = soup.find_all("p", class_="star-rating")[0].get("class")[1]
        mapping_rating[review_rating]
        rating_number = f"{review_rating} / 5"
        category = book_soup.find_all('li')[2].a.text
        article = book_soup.find('article')
        imgsrc = article.find("img").get("src")[6:]
        url_base = "https://books.toscrape.com/"
        image_url = url_base + imgsrc
        img_data = requests.get(image_url).content
        book = {'tracteur': title, 'description': description}
        all_books.append(book)

    return all_books


pg = 1
# je fais un objet soup avec l'url de l'accueil
# je cherche la valeur maximale de page que je rentre dans une variable pages_category = soup.find('li', class_="current").split()[2]
# je boucle sur le nombre de pages totales
for pg in range(51)
while pg :
    url = f"https://books.toscrape.com/catalogue/page-{pg}.html"
    soup_status = get_page(url)
    if soup_status[1] == 200:
        print(f" scraping page {pg}")
        links_temporary = get_links
        extract_info(get_links(soup_status[0]))
        pg += 1
    else:
        print("The End")
        break
    extract_info(all_books)
print(all_books)

