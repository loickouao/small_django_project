from .models import Stock, Price
import requests
from celery import shared_task

# import threading
from decouple import config
from bridger.notifications.models import Notification, NotificationSendType
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from django.conf import settings

print('task ok')
#Stock.objects.all().delete()
#Price.objects.all().delete()


@shared_task
def get_global_quote(namestock, test_msg_api = None, API_KEY = config('DO_ACCESS_APIKEY')):   
    if test_msg_api:
        price_response = test_msg_api
        print(price_response)

    else:
        if not API_KEY:
            raise Exception("Couldn't find DO_ACCESS_APIKEY environment variable!")
    
        #data: {'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}

        price_response = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+namestock+'&apikey='+API_KEY)
    data = price_response.json()
            

    #{'Error Message': 'Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for GLOBAL_QUOTE.'}
    if data.get('Error Message'):
        msg = f'Unknow Stock: {namestock} in the api AlphaVantage'
        print(msg)
        users = get_user_model().objects.all()
        for user in users:
            notif = Notification.objects.create(
                title = f'get_global_quote Stock: {namestock}',
                message = msg,
                send_type = NotificationSendType.SYSTEM.value,
                recipient = user,
            )
    else:
        DB = data.get('Global Quote')
        if DB :
            querystock = Stock.objects.all().filter(symbol = namestock)
            if querystock:
                response_stock = "Stock already exists in the database"
                insertstock = querystock[0]
            else:
                insertstock = Stock(symbol = DB.get("01. symbol"))
                insertstock.save()
                response_stock = "New Stock added to the database"
            print(namestock+": "+ response_stock)
        

            datetrading = DB.get('07. latest trading day')
            dateprice = Price.objects.all().filter(date = datetrading, stock = insertstock)
            if dateprice:
                response_price = "Price already added"
            else:
                insertprice = Price(open_price = DB.get('02. open'),
                high_price = DB.get('03. high'),
                low_price =  DB.get('04. low'),
                price = DB.get('05. price'),
                volume = DB.get('06. volume'),
                date = DB.get('07. latest trading day'))
                insertprice.stock = insertstock
                insertprice.save()
                response_price = "New Price added to the database"
            print(datetrading+": "+ response_price)              

            msg = f'{namestock}": {response_stock} \n {datetrading}": {response_price} '
        else:
            note = data.get('Note')
            msg = f'{note}'

        superuser = get_user_model().objects.create(
            username="test_user2", password="ABC", is_active=True, is_superuser=True
        )
        users = get_user_model().objects.all()
        
        print(users)
        for user in users:
            notif = Notification.objects.create(
                title = f'get_global_quote Stock: {namestock}',
                message = msg,
                send_type = NotificationSendType.SYSTEM.value,
                recipient = user,
                endpoint = reverse("djangoapp:stock-detail", args=[insertstock.pk])
            )
    print(notif)
    return notif


@shared_task() # name helps celery identify the functions it has to run
def run_parallel_get_global_quote():
    #stocks = ["IBM", "BABA", "BAC", "300135.SHZ"]
    stocks = Stock.objects.all()
    for stock in stocks:
        get_global_quote.delay(stock.symbol)
    # threads = [threading.Thread(target=get_global_quote, args=(stock.symbol,)) for stock in stocks]
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()

#run_parallel_get_global_quote.delay()
# run_parallel_get_global_quote.apply_async()