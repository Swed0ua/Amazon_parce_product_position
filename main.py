import requests
import time
from bs4 import BeautifulSoup
from time import sleep
import random
import json
import os
from quickstart import get_values
from quickstart import main
from datetime import date


_link = 'https://www.amazon.com'
start_link = f'https://www.amazon.com/s/query?crid=16RNRBBYXBQ2A&i=beauty-intl-ship'



headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

cookies = {"sp-cdn":"L5Z9:UA"}

def get_products_position ():
    data = get_values()
    products_sett = []
    for data_item in data:
        products_sett.append({"asin" : data_item[0], "search" : data_item[1]})
    tday = date.today()
    today = str(tday.strftime("%d.%m.%Y"))
    today = today.replace('-', '.')
    result_positions = [today]
    print('---------------START----------------')
    
    def search_in_pages (search):
        result_items = []
        for i in range(1, 1000):
            count = 0
            priv_link = f'{start_link}?i=beauty-intl-ship&k={search}&page={i}&qid=1675948760&ref=sr_pg_6'
            req = requests.get(priv_link, headers=headers, cookies=cookies)
            result = req.text.split('&&&')
            if len(result) <= 12 :
                break
            for index in range(0, len(result)-1):
                item = result[index]
                dispatch = json.loads(item)
                if dispatch[1].find('data-main-slot:search-result-') != -1:
                    result_items.append(dispatch)
                    item_html = dispatch[2]["html"]
                    soup = BeautifulSoup(item_html, 'lxml')
                    item_asin = soup.find('div').get('data-asin').strip()
                    if item_asin == asin:
                        print(f'YEEEEEEEEP | index such product = {len(result_items)}')
                        print('------------------------------------')
                        return len(result_items)
        return 0
    
    for product_sett in products_sett :
        asin = products_sett[0]["asin"] 
        search = product_sett["search"]
        result_index = search_in_pages(search)
        result_positions.append(result_index)
        
    print(result_positions)
    print('----------------END-----------------')
    main(result_positions)

get_products_position()