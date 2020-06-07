from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework import status
from djangoapp.serializers import PriceSerializer, StockSerializer
from django.urls import reverse
import pytest
import json

@pytest.mark.django_db
def test_create_stock_with_valid_data(client, stock_factory):
    """Tests POST method with valid data to create a stock instance."""

    stock = stock_factory(symbol = "stock_test")

    factory = APIRequestFactory()
    request = factory.get('/')

    context = {'request': Request(request)}

    stock_serializer = StockSerializer(stock, context=context)

    data = {
        'url': stock_serializer.data.get('url'),
        'symbol': stock_serializer.data.get('symbol'),
    }

    response = client.post(reverse('stock-list'),
                           data=json.dumps(data),
                           content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('symbol') == stock.symbol

@pytest.mark.django_db
def test_create_price_for_stock(client, stock_factory, price_factory):
    stock = stock_factory(symbol = "stock_test")
    price = price_factory(open_price=90.00, high_price=190.00, low_price=20.20, price=100.00, volume=40859, date="2020-06-03", stock = stock)

    factory = APIRequestFactory()
    request = factory.get('/')

    context = {'request': Request(request)}

    price_serializer = PriceSerializer(price, context=context)

    data = {
        'url': price_serializer.data.get('url'),
        'open_price':  price_serializer.data.get('open_price'),
        'high_price': price_serializer.data.get('high_price'),
        'low_price': price_serializer.data.get('low_price'),
        'price': price_serializer.data.get('price'),
        'volume': price_serializer.data.get('volume'),
    }

    response = client.post(reverse('price-list'),
                           data=json.dumps(data),
                           content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data['date'] = price_serializer.data.get('date')

    response = client.post(reverse('price-list'),
                           data=json.dumps(data),
                           content_type='application/json')
  
    assert response.status_code == status.HTTP_201_CREATED
