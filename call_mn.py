from py import get_products_position
import json
import time

def set_json(rs):
    with open('/var/www/html/scripts/my.json', 'w', encoding='utf-8') as file:
        rs["run"] = False
        file.write(json.dumps(rs))

def program_start (data):
    print('Call with admin panel')
    try:
        get_products_position(data)
    except Exception as e:
        print(f'ERR | Filed {e}')
        set_json(data)

while True:
    with open('/var/www/html/scripts/my.json', 'r', encoding='utf-8') as file:
        rs = file.read()
        rs = json.loads(rs)
    is_active = rs["run"]
    if is_active:
        program_start(data=rs)
        set_json(rs)
    time.sleep(5)

