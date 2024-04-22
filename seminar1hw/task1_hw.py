'''
Сбор и разметка данных (семинары)
Урок 1. Основы клиент-серверного взаимодействия. Парсинг API
1.Ознакомиться с некоторые интересными API. 
https://docs.ozon.ru/api/seller/ 
https://developers.google.com/youtube/v3/getting-started 
https://spoonacular.com/food-api
2.Потренируйтесь делать запросы к API. Выберите публичный API, который вас интересует, 
и потренируйтесь делать API-запросы с помощью Postman. 
Поэкспериментируйте с различными типами запросов и попробуйте получить различные типы данных.
3.Сценарий Foursquare
4.Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию 
(например, кофейни, музеи, парки и т.д.).
5.Используйте API Foursquare для поиска заведений в указанной категории.
6.Получите название заведения, его адрес и рейтинг для каждого из них.
7.Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.
'''

import requests
import json
import pandas as pd

client_id = "__"
client_secret = "__"

endpoint = "https://api.foursquare.com/v3/places/search"

city = input('Введите город => ')
# city = 'Moscow'
place = input('Введите заведение => ')
# place = 'museum'


params = {
    'client_id': client_id,
    'client_secret': client_secret,
    'near': city,
    'query': place
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

response = requests.get(endpoint, params=params, headers=headers)
if response.status_code == 200:
    
    data = json.loads(response.text)
    venues = data['results']
    
    # with open('data.json', 'w') as f:
    #     json.dump(venues, f, indent=2)
    
    some_list = []
    for ven in venues:
        try:
            some_list.append({'название': ven['name'], 'адрес': ven['location']['address'], 'категория': ven['categories'][0]['name']})
        except KeyError:
            some_list.append({'название': ven['name'], 'адрес': 'None'})
    
    df = pd.DataFrame(some_list)
else:
    print(response.status_code)

print(df.head(15))
