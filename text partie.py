import csv
from bs4 import BeautifulSoup
import requests
from csv import writer

url2 = 'https://books.toscrape.com/index.html'
page = requests.get(url2)
soup = BeautifulSoup(page.text, 'lxml')


def extract_info(link):
    # get informations for a book
    url = book_link
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Site non accessible")

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text()
    table = soup.find("table", {"class": "table table-striped"})
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


categories = {}

# Je récupére l'endroit dans la page ou est la liste de catégorie
side_categories = soup.find("ul", class_="nav-list")

# Je récupère les balises li à l'intérieur de cette balise ul
puces =side_categories.find_all("li")
# Find all retourne une list de balise li

# Pour chaque balise li, je récupère le titre de la catégorie et le lien
for puce in puces:
    link_in_puce = puce.find("a")
    name = link_in_puce.get_text # A verifier pour la correct syntaxe
    # Je stocke ma catégorie est lien dans un dictionnaire pour réutilisation plus tard
    categories[name] = link_in_puce.get("href")



links = []


def write_csv(books, category_name):
    # write on a csv file the informations about the books
    with open('category_name.csv', 'w') as csvfile:
        fieldnames = ['title', 'universal_product_code', 'url', 'PrixHT', 'PrixTTC', 'Stock', 'Description',
                      'Categorie', 'Note', 'UrlImage']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for book in books:
            writer.writerow(book)


for name, link in categories.items():
    url2 = link
    category_replace_html = link.replace("index.html", "")
    #pages_category = soup.find('li', class_="current").split()[2]
    books = []
    category_link = "https://books.toscrape.com/" + category_replace_html
    deuxieme_page_category = category_replace_html + "page-2"
    http_deuxieme_page = category_link + deuxieme_page_category
    page_deux_statut = requests.get(http_deuxieme_page)

    if page_deux_statut == 200 :
        # obtenir l'url de chaque page de la catégorie + extraire les infos
        for pg in range(pages_of_category):
            pg = 1
            pages_of_category = soup.find('li', class_="current").split()[2]
            urls_de_category = category_link + pages_of_category
            pg += 1
            category_pages_links = category_replace_html + f"page-{pg}"
            # obtenir l'url de chaque page de la catégorie + extraire les infos
            articles = soup.find_all('article', class_="product_pod")
            for article in articles:
                relative_book_url = article.find("h3").a.get("href")[9:]
                base_url = "https://books.toscrape.com/catalogue/"
                book_link = base_url + relative_book_url
                book_details = extract_info(book_link)
                books.append(book_details)

    else:
        articles = soup.find_all('article', class_="product_pod")
        for article in articles:
            relative_book_url = article.find("h3").a.get("href")[9:]
            base_url = "https://books.toscrape.com/catalogue/"
            book_link = base_url + relative_book_url
            book_details = extract_info(book_link)
            books.append(book_details)

    write_csv(books)

"""  #refaire un objet soup pour trouver current
    #si current ='none' alors extraire sinon(else) => Split
    #extraire
        # loop dans differentes pages d'une catégorie
    for pg in range(pages_category):
        pg += 1
        category_full = category_new + f"page-{pg}"
        response = requests.get(category_full)
        soup = BeautifulSoup(response.content, 'lxml')
        # obtenir l'url de chaque page de la catégorie + extraire les infos
        articles = soup.find_all('article', class_="product_pod")
        for article in articles:
                relative_book_url = article.find("h3").a.get("href")[9:]
                base_url = "https://books.toscrape.com/catalogue/"
                book_link = base_url + relative_book_url
                book_details = extract_info(book_link)
                books.append(book_details)"""