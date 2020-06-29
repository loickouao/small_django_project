import pytest
from djangoapp.tasks import run_parallel_get_global_quote, get_global_quote
from unittest.mock import patch
from djangoapp.models import Stock, Price
from bridger.notifications.models import Notification, NotificationSendType
from django.contrib.auth import get_user_model

# import requests
# import requests_mock

# @requests_mock.Mocker()
# def mock_request_api(m, stock, price):
#     if price:
#         msg_api = {
#             "Global Quote": {
#                 "01. symbol": stock.symbol,
#                 "02. open": price.open_price,
#                 "03. high": price.high_price,
#                 "04. low": price.low_price,
#                 "05. price": price.price,
#                 "06. volume": price.volume,
#                 "07. latest trading day": price.date,
#             }
#         }
#     else:
#         msg_api = {
#             "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for GLOBAL_QUOTE."
#         }
#     m.get('http://test-alphavantage.ch', text=msg_api)
#     return requests.get('http://test-alphavantage.ch').text

# def mock_request_api2(stock, price):
#     if price:
#         msg_api = {
#             "Global Quote": {
#                 "01. symbol": stock.symbol,
#                 "02. open": price.open_price,
#                 "03. high": price.high_price,
#                 "04. low": price.low_price,
#                 "05. price": price.price,
#                 "06. volume": price.volume,
#                 "07. latest trading day": price.date,
#             }
#         }
#     else:
#         msg_api = {
#             "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for GLOBAL_QUOTE."
#         }
#     with requests_mock.Mocker() as m:
#         m.get('http://test-alphavantage.ch', text=msg_api)
#         return requests.get('http://test-alphavantage.ch').text




@pytest.mark.django_db
class Test_global_quote:
    def get_user(self):
        superuser = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )
        return superuser

    
    def test_notification(self, stock_factory, price_factory):
        stock = stock_factory(symbol="IBM")
        stock2 = stock_factory()
        # price = price_factory(stock)
        # msg_api = mock_request_api2(stock, price)

        # notification = get_global_quote(stock.symbol, test_msg_api = msg_api)
        notif = get_global_quote(stock.symbol)
        notif2 = get_global_quote(stock2.symbol)

        user = self.get_user()
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
        assert notif.title == notification.title 
        assert notif2.title == notification2.title 




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

