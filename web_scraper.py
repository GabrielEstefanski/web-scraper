import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

url = "https://www.kabum.com.br/espaco-gamer/cadeiras-gamer"

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome / 114.0.0.0 Safari / 537.36"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qty_items = soup.find('div', id='listingCount').get_text().strip()

index = qty_items.find(' ')
qty = qty_items[:index]

last_page = math.ceil(int(qty)/20)

dict_products = {'brand':[], 'price':[]}

for i in range(1, last_page+1):
    url_page = f"https://www.kabum.com.br/espaco-gamer/cadeiras-gamer?page_number={i}&page_size=20&facet_filters=&sort=most_searched"
    site = requests.get(url_page, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    products = soup.find_all('div', class_=re.compile('productCard'))

    for product in products:
        brand = product.find('span', class_=re.compile('nameCard')).get_text().strip()
        price = product.find('span', class_=re.compile('priceCard')).get_text().strip()

        print(brand, price)

        dict_products['brand'].append(brand)
        dict_products['price'].append(price)
    print (url_page )

df = pd.DataFrame(dict_products)
df.to_csv('C:/Users/R31_d0_R0CK/Desktop/web-scraper/cadeiras_gamer.csv', encoding='utf-8', sep=';')

