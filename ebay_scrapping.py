"""
# TODO
# 1. Make a request to ebay.com and get a page
# 2. Collect data from each detail page
# 3. Collect all links to detail pages of each product
# 4. Write scraped data to a csv file
"""

import requests
from bs4 import BeautifulSoup
import csv
# import pandas
import time


def get_page_number(url):
    soup = get_page(url)
    page_nr = soup.find("h1", {"class": "srp-controls__count-heading"}).find("span", {"class": "BOLD"}).text
    page_nr = int(page_nr.replace(",", ""))
    page_nr = page_nr if page_nr < 10000 else 10000
    items_per_page = int(soup.find("div", {"class": "srp-ipp__control--legacy"}).find('span').text)
    pages = int(page_nr / items_per_page) + 1
    # print(pages)
    # Only 200 as ebay allows maximum of 200 pages
    pages = pages if pages < 200 else 200
    print(pages)
    return pages


def get_page(url):
    response = requests.get(url)

    # print(response.ok)
    # print(response.status_code)
    if not response.ok:
        print('Server responded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    """
    # Method to Get following
    # title
    # price
    # Items Sold
    """
    # h1 = soup.find('h1, id='itemTitle').find('a').get('data-mtdes')
    try:
        title = soup.find("h1", {"id": "itemTitle"}).find("span", {"class": "g-hdn"}).next_sibling
    except:
        title = ""

    try:
        try:
            p = soup.find('span', {'id': "prcIsum"}).text.strip()
        except:
            p = soup.find('span', {'id': "mm-saleDscPrc"}).text.strip()
        currency, price = p.split(' ')
    except:
        price = ''
        currency = ''

    try:
        sold = soup.find('span', {'class': "vi-qtyS-hot-red"}).find('a').text.strip().split(' ')[0]
    except:
        sold = ''

    # print(title)
    # print(currency, price)
    # print(sold)

    data = {
        'title': title,
        'price': price,
        'currency': currency,
        'total sold': sold
    }

    return data


def get_index_data(soup):
    try:
        links = soup.find_all('a', {'class': 's-item__link'})
    except:
        links = []

    urls = [item.get('href') for item in links]

    # print(urls)
    return urls


def write_csv(data, url):
    with open('ebay_output.csv', 'a', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        row = [data['title'], data['price'], data['currency'], data['total sold'], url]
        writer.writerow(row)


def main():
    url = "https://www.ebay.com/sch/i.html?kw=men+watches&_sacat&_pgn=1"

    total_pages = get_page_number(url)

    # soup = get_page(url)
    # get_detail_data(get_page(url))

    for i in range(1, total_pages+1):
        print(i)
        "https://www.ebay.com/sch/i.html?kw=men+watches&_sacat&_pgn=" + str(i)
        products = get_index_data(get_page(url))
        time.sleep(1)

        # print(len(products))

        # list_details = []

        for link in products:
            data = get_detail_data(get_page(link))
            write_csv(data, link)
            # print(data)
            # list_details.append(data)

        # df = pandas.DataFrame(list_details)
        # df.to_csv("Ebay_Output.csv")
        # print(df)


if __name__ == "__main__":
    main()
