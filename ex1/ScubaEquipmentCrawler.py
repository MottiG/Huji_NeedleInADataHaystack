import requests as rq
from bs4 import BeautifulSoup as Bs
import re
import json
import time

NUM_OF_PRODUCTS = 50
SEC_TO_WAIT = 3  # number of second to wait between requests
IDX_OF_CATEGORY = 0
STORE_URL = "http://www.divers-supply.com"
PRODUCTS_PAGE_LIMIT = {'limit': '48'} # number of products per page

headers = {"X-Requested-With": "XMLHttpRequest",
         'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


# TODO work on reviews:
raw_page2 = rq.get("http://www.divers-supply.com/scuba-gear/bcd/cressi-ultralight-lady-bcd.html", headers=headers)
page2 = Bs(raw_page2.content)
scripts = page2.find_all('script', {'type': 'text/javascript'})
script = None
for s in scripts:
    if len(s.contents) > 0 and str(s.contents[0]).find('tbConfig'):
        script = s

print(page2.prettify())
prod = {}
rev_div = page2.find_all('div', {'class': 'targetbay-review-lists'})
gd = None
# end of work


def retrieve_categories_links(url: str) -> list:
    print("GETS CATEGORIES")  # TODO dell
    time.sleep(SEC_TO_WAIT)
    raw_page = rq.get(url).content
    page = Bs(raw_page, 'lxml')
    categories_list = page.find('div', {'class': 'easycatalogimg'}).find_all('h5')
    links_of_categories = [category.contents[IDX_OF_CATEGORY].get('href') for category in categories_list]
    return links_of_categories


def retrieve_products_links(sublink: str, products_to_update: list) -> None:
    print("GETS PROD_LINKS")  # TODO dell
    time.sleep(SEC_TO_WAIT)
    raw_products_page = rq.get(sublink, params=PRODUCTS_PAGE_LIMIT).content
    product_page = Bs(raw_products_page, 'lxml')
    next_btn = product_page.find('a', {'class': 'next i-next'})

    for prod in product_page.find_all('h2', {'class': 'product-name'}):
        products_to_update.append(prod.a.get('href'))
        if len(products_to_update) >= NUM_OF_PRODUCTS:
            return

    if next_btn:
        retrieve_products_links(next_btn.get('href'), products_to_update)


def retrieve_product_json(prod_link: str) -> json:
    print("GETS JSONS")  # TODO dell
    time.sleep(SEC_TO_WAIT)
    prod_dict = dict()
    prod_dict['Url'] = prod_link
    raw_page = rq.get(prod_link).content
    page = Bs(raw_page, 'lxml')
    title = page.title.string.split(" - ")
    name = title[0].strip()
    sub_category = title[1].strip()
    category = title[2].strip()
    price = page.find('div', {'class': 'price-box'}).find_all('span', {'class': 'price'})
    im = page.find('div', {'class': 'product-img-box'}).find('a').get('href')
    name = page.find('div', {'class': 'product-name'}).find('h1').contents
    desc_lines = page2.find('div', {'class': 'product-collateral'}).find('div', {'class': 'std'}).find_all('p')
    desc = ""
    for p in desc_lines:
        for line in p.strings:
            desc += line
    if len(price) > 1:
        prod_dict['Price'] = {'Old Price': price[0].contents[0].strip(), 'Sale Price': price[1].contents[0].strip()}
    else:
        prod_dict['Price'] = price[0].contents[0].strip()


#
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





