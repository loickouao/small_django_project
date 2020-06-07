from django.test import TestCase

# Create your tests here.
import pytest

#pytest.mark.django_db is a decorator provided by pytest-django that gives the test write access to the database.
@pytest.mark.django_db
def test_stock_model(stock_factory):
    # create stock model instance
    stock = stock_factory(symbol="symbol_test_stock")    
    assert stock.symbol == "symbol_test_stock"

@pytest.mark.django_db
def test_price_model(stock_factory, price_factory):
    # create stock and price model instances
    stock = stock_factory(symbol="symbol_test_stock")
    price = price_factory(open_price=90.00, high_price=190.00, low_price=20.20, price=100.00, volume=40859, date="2020-06-03", stock = stock)

    assert price.stock == stock
    assert price.stock.symbol == "symbol_test_stock"
    assert price.open_price == 90.00
    assert price.high_price == 190.00
    assert price.low_price == 20.20
    assert price.price == 100.00
    assert price.volume == 40859
    assert price.date == "2020-06-03"


