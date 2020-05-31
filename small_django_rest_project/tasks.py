from .models import Stock, Price
from celery.decorators import task
import requests
from celery import shared_task
import time

print('task ok')
#Stock.objects.all().delete()
#Price.objects.all().delete()


def global_quote(API_KEY = '7MBXGSIZSE5KT31D'):
    cpt_for_calls = 0
    #data: {'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}
    for s in ["IBM", "BABA", "BAC", "300135.SHZ"]:
        cpt_for_calls = cpt_for_calls + 1
        if cpt_for_calls == 5:
            print("sleep!! wait 65 seconds ")
            time.sleep(65)
            cpt_for_calls = 0    
        price_response=requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+s+'&apikey='+API_KEY)
        data = price_response.json()
        #print(data)
        try :
            print(data['Global Quote'])
        except:
            print(data['Note'])
            return 0

        querystock = Stock.objects.all().filter(symbol = s)
        if querystock:
            print("Stock exist")
            insertstock = querystock[0]
        else:
            insertstock = Stock(symbol = data['Global Quote']["01. symbol"])
            insertstock.save()

        dateprice = Price.objects.all().filter(date = data['Global Quote']['07. latest trading day'], stock = insertstock)
        if dateprice:
            print("Price exist")
        else:
            insertprice = Price(open_price = data['Global Quote']['02. open'],
            high_price = data['Global Quote']['03. high'],
            low_price =  data['Global Quote']['04. low'],
            price = data['Global Quote']['05. price'],
            volume = data['Global Quote']['06. volume'],
            date = data['Global Quote']['07. latest trading day'])
            insertprice.stock = insertstock
            insertprice.save()

global_quote()

@task
def global_quote_celery():
    print('tasks fn')

@task(name='add')
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    print('add tasks inside')
    for i in range(10):
        a = x+y
    return x+y
"""
# celery
#global_quote_celery()
#add.apply_async(1,1) #error type
#add.delay(1,1) #stacks forever
#global_quote_celery.delay()
"""