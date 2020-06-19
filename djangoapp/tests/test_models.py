# from django.test import TestCase
from django.utils import timezone
import pytest
from datetime import timedelta

#pytest.mark.django_db is a decorator provided by pytest-django that gives the test write access to the database.
@pytest.mark.django_db
class Test_stock_model:
    def test_field_stock(self, stock_factory):
        # create stock model instance
        stock0 = stock_factory()
        stock = stock_factory(symbol="symbol_test_stock")    

        assert stock0.id is not None
        assert stock.symbol == "symbol_test_stock"

    def test_str(self, stock_factory):
        stock0 = stock_factory()
        assert str(stock0) == stock0.symbol
        
@pytest.mark.django_db
class Test_price_model:
    def test_field_price(self, stock_factory, price_factory):
        # create stock and price model instances
        price0 = price_factory()

        stock = stock_factory(symbol="symbol_test_stock")
        date = timezone.now().date()
        datetime = timezone.now() 
        price = price_factory(open_price=90.00, high_price=190.00, low_price=20.20, price=100.00, volume=40859, date=date, datetime=datetime, stock = stock)


        assert price0.pk is not None
        assert price0.stock.pk is not None
        assert price0.date == date
        assert price0.datetime.strftime("%Y-%m-%d %H:%M:%S") == datetime.strftime("%Y-%m-%d %H:%M:%S")
        

        assert price.stock == stock
        assert price.stock.symbol == "symbol_test_stock"
        assert price.open_price == 90.00
        assert price.high_price == 190.00
        assert price.low_price == 20.20
        assert price.price == 100.00
        assert price.volume == 40859
        assert price.date == date
        assert price.datetime.strftime("%Y-%m-%d %H:%M:%S") == datetime.strftime("%Y-%m-%d %H:%M:%S")


    def test_str(self, price_factory):
        price0 = price_factory(price=100.95)
        assert str(price0) == "100.95"



# @pytest.mark.django_db
# def test_get_nb_prices_stock_date(stock_factory):
#     stock = stock_factory()
#     nb_stock = stock.get_nb_prices_stock_date("2020-06-19")
#     stock.nb_prices_today
#         nb_prices_today = nb_stock
#     )
#     assert stock.nb_prices_today is not None
#     assert stock.symbol == nb_stock
