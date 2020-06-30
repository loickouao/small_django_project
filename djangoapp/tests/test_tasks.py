import pytest
from djangoapp.tasks import run_parallel_get_global_quote, get_global_quote
from unittest.mock import patch
from djangoapp.models import Stock, Price
from bridger.notifications.models import Notification, NotificationSendType
from django.contrib.auth import get_user_model
import json
from decouple import config

import requests

def get_mock_stock(namestock, result = None, API_KEY = config('DO_ACCESS_APIKEY')):
    USERS_URL = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+namestock+'&apikey='+API_KEY
    """Get list of users"""
    response = requests.get(USERS_URL)
    if response.ok:
        result = response
    return result

@pytest.mark.django_db
class Test_global_quote:
    def get_user(self):
        superuser = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )
        return superuser

    @patch('requests.get') 
    def testMock_request_response(self, mock_get):
        data = {'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}

        mock_get.return_value.status_code = 200 # Mock status code of response.
        mock_get.return_value.json.return_value = data
        response = get_mock_stock("IBM")

        # Assert that the request-response cycle completed successfully with status code 200.
        assert response.status_code == 200
        assert response.json() == data

        user = self.get_user()
        notif = get_global_quote("BABA", price_response=response, user=user )
        notification = Notification.objects.create(
            recipient = user,
            title = f'get_global_quote Stock: BABA',
            message = "You have a new notification",
        )
        assert str(notif) == str(notification) 

   
    def test_notification(self, stock_factory, price_factory):
        stock = stock_factory(symbol="IBM")
        stock2 = stock_factory()
        # price = price_factory(stock)
        # msg_api = mock_request_api2(stock, price)

        # notification = get_global_quote(stock.symbol, test_msg_api = msg_api)
        user = self.get_user()
        notif = get_global_quote(stock.symbol, user=user)
        notif2 = get_global_quote(stock2.symbol, user=user)

        get_global_quote("BABA", user=user)
        
        patch("celery.execute.send_task")
        notification = Notification.objects.create(
            recipient = user,
            title = f'get_global_quote Stock: {stock.symbol}',
            message = "You have a new notification",
        )
        notification2 = Notification.objects.create(
            recipient = user,
            title = f'get_global_quote Stock: {stock2.symbol}',
            message = "You have a new notification",
        )
        assert str(notif) == str(notification) 
        assert str(notif2) == str(notification2) 



    @patch('djangoapp.tasks.get_global_quote.delay')
    def test_run_parallel_get_global_quote(self, get_global_quote, stock_factory, price_factory):
        stock_factory(symbol = "IBM")
        stock = stock_factory(symbol = "BABA")
        
        run_parallel_get_global_quote()
        # assert get_global_quote is run_parallel_get_global_quote

        # assert get_global_quote.called # Check that the function was called
        get_global_quote.assert_called()
        get_global_quote.assert_called_with(stock.symbol)

        assert get_global_quote.call_count == 2

