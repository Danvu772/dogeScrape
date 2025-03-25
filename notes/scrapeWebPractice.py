import requests
from bs4 import BeautifulSoup 
import time
import pandas as pd
import re

def main():

    url = 'https://books.toscrape.com/'

    hugeLib = []

    hugeLib += grabAllBooks(url)

    for i in range(2, 51):
        pageUrl = f'catalogue/page-{i}.html'
        hugeLib += grabAllBooks(url+pageUrl)

    df = pd.DataFrame(hugeLib)
    df.to_csv('output.csv', index=False)
    print('created csv')


def grabAllBooks(url):

    starMap = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

    r = requests.get(url)
    print('getting: ' + url + pageUrl)

    soup = BeautifulSoup(r.content, 'html.parser')

    titles = soup.select('li h3 a')
    prices = soup.select('.product_price .price_color')
    ratings = soup.select('.star-rating')

    dict = []

    for i in range(len(titles)):

        title = titles[i].get('title')
        price = float(prices[i].text.strip()[1:])
        rating = starMap[ratings[i].get('class')[-1]]
        bpUrl = titles[i].get('href')

        bp = requests.get(url + bpUrl)
        print('getting: ' + url + bpUrl)

        bpSoup = BeautifulSoup(bp.content, 'html.parser')

        UPC = bpSoup.find(lambda tag:tag.name=='th' and tag.text.strip() == 'UPC').find_next_sibling().text.strip()
        available = bpSoup.find(lambda tag:tag.name=='th' and tag.text.strip() == 'Availability').find_next_sibling().text.strip()
        available = int(re.search(r'\b(\d+)\s+available', available).group(1))
        productType =  bpSoup.find(lambda tag:tag.name=='th' and tag.text.strip() == 'Product Type').find_next_sibling().text.strip()

        dict.append({'Title': title, 'Price': price, 'Rating': rating, 'UPC': UPC, 'Available': available, 'Product Type': productType})

    return dict
    


main()

