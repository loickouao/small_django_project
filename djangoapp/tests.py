from django.test import TestCase

# Create your tests here.
from .models import Stock, Price
import pytest
import os
import dotenv

from .factories import StockFactory, PriceFactory

@pytest.mark.django_db
def test_stock_model():
    # create stock model instance
    stock = StockFactory(symbol="Test Stock Symbol")    
    
    assert stock.symbol == "Test Stock Symbol"


@pytest.mark.django_db
def test_price_model():
    # create stock and price model instances
    stock = StockFactory(symbol="Test Stock Symbol")
    price = PriceFactory(open_price=90.00, high_price=190.00, low_price=20.20, price=100.00, volume=40859, date="2020-06-03", stock = stock)

    assert price.stock == stock
    assert price.stock.symbol == "Test Stock Symbol"
    assert price.open_price == 90.00
    assert price.high_price == 190.00
    assert price.low_price == 20.20
    assert price.price == 100.00
    assert price.volume == 40859
    assert price.date == "2020-06-03"
