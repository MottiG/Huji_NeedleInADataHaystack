import requests as rq
from bs4 import BeautifulSoup as Bs
import json
import time

NUM_OF_PRODUCTS = 50  # total number of products
PRODUCTS_PER_SUBCATEGORY = 2  # number of products per category - to allow diversity of categories
SEC_TO_WAIT = 3  # number of second to wait between requests
IDX_OF_CATEGORY = 0
STORE_URL = "http://www.divers-supply.com"
PRODUCTS_PAGE_LIMIT = {'limit': '48'} # number of products per page


def retrieve_categories_links(url: str) -> list:
    """
    retrieve links of categories\sub-categories
    :param url: parent page url
    :return: list contain the links
    """
    time.sleep(SEC_TO_WAIT)
    raw_page = rq.get(url).content
    page = Bs(raw_page, 'lxml')
    categories_list = page.find('div', {'class': 'easycatalogimg'}).find_all('h5')
    links_of_categories = [category.contents[IDX_OF_CATEGORY].get('href') for category in categories_list]
    return links_of_categories


def create_product_dict(prod_link: str) -> dict:
    """
    create dictionary of a product
    :param prod_link: product url
    :return: dictionary represent the product
    """
    time.sleep(SEC_TO_WAIT)
    prod_dict = dict()
    raw_page = rq.get(prod_link).content
    page = Bs(raw_page, 'lxml')
    details = page.find('div', {'class': 'breadcrumbs'})
    categories = details.find_all('a')
    price = page.find('div', {'class': 'price-box'}).find_all('span', {'class': 'price'})
    prod_dict['URL'] = prod_link
    prod_dict['Title'] = details.find('strong').text.strip()
    prod_dict['Category'] = categories[1].text.strip()
    prod_dict['Sub-Category'] = categories[2].text.strip()
    prod_dict['Price'] = price[0].contents[0].strip()
    prod_dict['Sale-Price'] = price[1].contents[0].strip() if len(price) > 1 else 'None'
    prod_dict['Image URL'] = page.find('div', {'class': 'product-img-box'}).find('a').get('href')
    try:
        prod_dict['Description'] = page.find('div', {'class': 'product-collateral'}).find('div', {'class': 'std'}).text.strip()
    except AttributeError: # in case there is no description
        prod_dict['Description'] = "None"
    return prod_dict


def retrieve_products(sublink: str, products_to_update: list) -> None:
    """
    retrieve the products pages of a given sub-category and fill the 'products_to_update' list with the dicts of them
    :param sublink: the sub-category link
    :param products_to_update: list to fill with the products dicts
    :return: None
    """
    time.sleep(SEC_TO_WAIT)
    prod_of_sublink_sum = 0
    raw_products_page = rq.get(sublink, params=PRODUCTS_PAGE_LIMIT).content
    product_page = Bs(raw_products_page, 'lxml')
    next_btn = product_page.find('a', {'class': 'next i-next'})

    for prod in product_page.find_all('h2', {'class': 'product-name'}):
        prod_link = prod.a.get('href')
        products_to_update.append(create_product_dict(prod_link))
        prod_of_sublink_sum += 1
        if len(products_to_update) >= NUM_OF_PRODUCTS or prod_of_sublink_sum == PRODUCTS_PER_SUBCATEGORY:
            return

    if next_btn:
        retrieve_products(next_btn.get('href'), products_to_update)


if __name__ == '__main__':

    products = list()  # list of dicts
    list_of_categories_links = retrieve_categories_links(STORE_URL)

    for link in list_of_categories_links:
        subcategories_links = retrieve_categories_links(link)
        for sub_link in subcategories_links:
            if len(products) < NUM_OF_PRODUCTS:
                retrieve_products(sub_link, products)

    with open(str(NUM_OF_PRODUCTS)+'_products_'+str(PRODUCTS_PER_SUBCATEGORY)+'_per_subcategory.json', 'w') as fp:
        json.dump(products, fp, indent=4, sort_keys=True, ensure_ascii=False)



