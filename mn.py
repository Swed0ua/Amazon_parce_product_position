import schedule
from py import get_products_position
import time
import json

total = 0

def call_to() :
    global total
    total += 1

    try:
        with open(f'/var/www/html/scripts/main.json', 'r', encoding='utf-8') as file:
            rd = file.read()
            rd = json.loads(rd)
        for rs in rd:
            get_products_position(rs)
            print('Success | Request completed successfully')
    except Exception as e:
        print(f'Error | {e}')


def prog():
    schedule.every().day.at("09:15").do(call_to)
    #schedule.every().day.at("06:00").do(call_to)
    while True:
        schedule.run_pending()
        time.sleep(1)

prog()