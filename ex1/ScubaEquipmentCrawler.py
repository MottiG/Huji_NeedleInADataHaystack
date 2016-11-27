import requests as rq
from bs4 import BeautifulSoup as Bs
import json
import time

NUM_OF_PRODUCTS = 50
SEC_TO_WAIT = 3  # number of second to wait between requests
IDX_OF_CATEGORY = 0
STORE_URL = "http://www.divers-supply.com"
PRODUCTS_PAGE_LIMIT = {'limit': '48'} # number of products per page

raw_page = rq.get("http://www.divers-supply.com/scuba-gear/computers/mares-dive-computer-nemo-wide.html").content
page = Bs(raw_page, 'lxml')
details = page.title.string.split(' - ')
if details[0][-1] == " ":
    details[0] = details[0][:-1]
im = page.find('img', {'alt': details[0]}).get('src')
#todo check problem with name if product
price = page.find('div', {'class': 'price-box'}).find_all('span', {'class': 'price'})
prod = {}

#
#
# def retrieve_categories_links(url: str) -> list:
#     print("GETS CATEGORIES")  # TODO dell
#     time.sleep(SEC_TO_WAIT)
#     raw_page = rq.get(url).content
#     page = Bs(raw_page, 'lxml')
#     categories_list = page.find('div', {'class': 'easycatalogimg'}).find_all('h5')
#     links_of_categories = [category.contents[IDX_OF_CATEGORY].get('href') for category in categories_list]
#     return links_of_categories
#
#
# def retrieve_products_links(sublink: str, products_to_update: list) -> None:
#     print("GETS PROD_LINKS")  # TODO dell
#     time.sleep(SEC_TO_WAIT)
#     raw_products_page = rq.get(sublink, params=PRODUCTS_PAGE_LIMIT).content
#     product_page = Bs(raw_products_page, 'lxml')
#     next_btn = product_page.find('a', {'class': 'next i-next'})
#
#     for prod in product_page.find_all('h2', {'class': 'product-name'}):
#         products_to_update.append(prod.a.get('href'))
#         if len(products_to_update) >= NUM_OF_PRODUCTS:
#             return
#
#     if next_btn:
#         retrieve_products_links(next_btn.get('href'), products_to_update)
#
#
def retrieve_product_json(prod_link: str) -> json:
    print("GETS JSONS")  # TODO dell
    time.sleep(SEC_TO_WAIT)
    raw_page = rq.get(prod_link).content
    page = Bs(raw_page, 'lxml')
    prod_title = page.title.string.split(' - ')
    im_link = page.find('img', {'alt': prod_title[0]}).get('src')
    prod = {}
    prod['Title'] = prod_title[0]
    prod['Sub-Category'] = prod_title[1]
    prod['Category'] = prod_title[2]
    prod['Image-Url'] = im_link



#
#     # TODO finish json builder
#
#
# list_of_categories_links = retrieve_categories_links(STORE_URL)
# products_links = []
# products_jsons = []
#
#
# for link in list_of_categories_links:
#     subcategories_links = retrieve_categories_links(link)
#     for sub_link in subcategories_links:
#         if len(products_links) < NUM_OF_PRODUCTS:
#             retrieve_products_links(sub_link, products_links)
#
#
# for prod_link in products_links:
#     products_jsons.append(retrieve_product_json(prod_link))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
