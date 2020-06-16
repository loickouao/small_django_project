from .models import Stock, Price
import requests
from celery import shared_task
import time
import threading
from decouple import config
from bridger.notifications.models import Notification, NotificationSendType

print('task ok')
#Stock.objects.all().delete()
#Price.objects.all().delete()

start = time.time()

def get_global_quote(namestock, API_KEY = config('DO_ACCESS_APIKEY')):   
    if not API_KEY:
        raise Exception("Couldn't find DO_ACCESS_APIKEY environment variable!")
 
    #data: {'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}
    price_response = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+namestock+'&apikey='+API_KEY)
    data = price_response.json()
    
    DB = data.get('Global Quote')
    if DB :
        querystock = Stock.objects.all().filter(symbol = namestock)
        if querystock:
            print(namestock+": Stock already exists in the database")
            insertstock = querystock[0]
        else:
            insertstock = Stock(symbol = DB.get("01. symbol"))
            insertstock.save()
            print(namestock+ ": New Stock added to the database")              

        datetrading = DB.get('07. latest trading day')
        dateprice = Price.objects.all().filter(date = datetrading, stock = insertstock)
        if dateprice:
            print(datetrading+ ": Price already added")
        else:
            insertprice = Price(open_price = DB.get('02. open'),
            high_price = DB.get('03. high'),
            low_price =  DB.get('04. low'),
            price = DB.get('05. price'),
            volume = DB.get('06. volume'),
            date = DB.get('07. latest trading day'))
            insertprice.stock = insertstock
            insertprice.save()
            print(datetrading+ ": New Price added to the database")              
    else:
        print(DB, data.get('Note')) 

    #print("'%s\' fetched in %ss" % (namestock, (time.time() - start))) 


@shared_task() # name helps celery identify the functions it has to run
def run_parallel_get_global_quote():
    #stocks = ["IBM", "BABA", "BAC", "300135.SHZ"]
    stocks = Stock.objects.all()
    threads = [threading.Thread(target=get_global_quote, args=(stock.symbol,)) for stock in stocks]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Notification.objects.create(
    #     title = "Notification task prices for each stock",
    #     message = "You have a new notification",
    #     recipient = user,
    #     send_type = NotificationSendType.SYSTEM_AND_MAIL.value,
    #     endpoint = get_full_widget_url(reverse("crm:activity-detail", args = [activity.id]))
    # )

#run_parallel_get_global_quote.delay()
# run_parallel_get_global_quote.apply_async()



