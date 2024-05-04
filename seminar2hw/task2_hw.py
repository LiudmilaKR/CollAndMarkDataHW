'''
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте 
во всех категориях: название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
Затем сохранить эту информацию в JSON-файле.
'''

import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import re

cur_page_url = 'http://books.toscrape.com/'

common_list = []
while True:
    # print('-----------------------------------')
    # print('cur_page_url=', cur_page_url)
    resp = requests.get(cur_page_url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    # with open('index.html', 'w', encoding='utf-8') as f:
    #     f.write(soup.prettify())
    

    for item in soup.find_all('article', class_='product_pod'):
        item_dict = {}
        
        item_name = item.find('h3').find('a')
        item_dict['title'] = item_name.get('title') if item_name else 'None'
        item_url = item_name.get('href') if item_name else ''
        
        item_price = item.find('div', class_='product_price').find('p', class_='price_color')
        item_dict['price'] = item_price.text if item_price else 'None'

        if item_url != '':
            item_full_url = urllib.parse.urljoin(cur_page_url, item_url)
        
        if item_full_url:
            resp_item = requests.get(item_full_url)
            soup_item = BeautifulSoup(resp_item.content, 'html.parser')
            item_q = soup_item.find('p', class_='instock availability')
            item_q = item_q.text.strip() if item_q else 0
            item_q = int(re.sub('[^0-9]', '', item_q))
            item_dict['qauntity'] = item_q
            
            item_d = soup_item.find('div', class_='sub-header').findNext('p')
            item_d = item_d.text if item_d else 'None'
            item_dict['description'] = item_d
        # print(item_name.get('title'))
        # print(item_dict)
        common_list.append(item_dict)
    
    next_page = soup.find('li', ('class', 'next'))
    if next_page:
        next_page_url = next_page.find('a').get('href')
        print('next_page_url=', next_page_url)
        cur_page_url = urllib.parse.urljoin(cur_page_url, next_page_url)
    else:
        break

with open('books.json', 'w', encoding='utf-8') as f:
    json.dump(common_list, f, indent=2)
    