from py import get_products_position
import time

total = 0

def call_to() :
    global total
    total += 1

    try:
        get_products_position()
        print('Success | Request completed successfully')
    except Exception as e:
        print(f'Error | {e}')


def prog():
   get_products_position()

prog()