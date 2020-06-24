from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework import status
from djangoapp.serializers import (
    StockRepresentationModelSerializer, StockModelSerializer, PriceRepresentationModelSerializer, PriceModelSerializer, NbPriceStockModelSerializer, MultiplyPricesActionButtonSerializer)
from django.urls import reverse
import pytest
import json
from bridger.serializers import AdditionalResourcesField, HyperlinkField 

@pytest.mark.django_db
class TestStockRepresentationModelSerializer:
    def test_fields(self, stock_factory):
        stock = stock_factory()
        serializer_data = StockRepresentationModelSerializer(stock).data
        assert set(serializer_data.keys()) == set(['id', 'symbol', '_detail'])
        assert serializer_data['id'] is not None
        assert serializer_data['symbol'] is not None
        assert serializer_data['_detail'] is not None


@pytest.mark.django_db
class TestStockModelSerializer:
    def test_fields(self, stock_factory):
        stock = stock_factory()
        factory = APIRequestFactory()
        request = factory.get("")
        serializer_data = StockModelSerializer(stock, context= {'request': Request(request)}).data
        assert set(serializer_data.keys()) == set(['id', 'symbol', 'prices', '_additional_resources'])
        assert serializer_data.get('id') is not None
        assert serializer_data.get('symbol') is not None
        assert serializer_data.get('prices') is not None
        assert serializer_data.get('_additional_resources') is not None

    def test_additionnal_resources(self, stock_factory):
        stock = stock_factory()
        factory = APIRequestFactory()
        request = factory.get("")
        serializer_data = StockModelSerializer(stock, context= {'request': Request(request)}).data
        ressource = serializer_data.get("_additional_resources")
        assert set(ressource.keys()) == set(['prices', 'modifyprices', 'chartprices'])
        assert ressource.get("prices") is not None
        assert ressource.get("modifyprices") is not None
        assert ressource.get("chartprices") is not None

    def test_StockModelSerializerViewset(self, admin_client, stock_factory):
        """Tests POST method with valid data to create a stock instance."""
        stock = stock_factory()
        factory = APIRequestFactory()
        request = factory.get('')
        #user = get_user_model().objects.create(username='some_user', is_superuser=True, is_active=True)
        #request.user = user
        #context = {'request': request}
        context = {'request': Request(request)}
        stock_serializer = StockModelSerializer(stock, context = context)

        response = admin_client.post(reverse('djangoapp:stock-list'),
                            json.dumps(stock_serializer.data),
                            content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED
        assert set(response.json().get('instance').keys()) == set(["id", "symbol", "prices", "_additional_resources"])
        assert response.json().get('instance').get('id') == stock.id + 1  == stock_serializer.data.get('id') + 1 #Method POST create new object
        assert response.json().get('instance').get('symbol') == stock.symbol == stock_serializer.data.get('symbol')
        assert len(response.json().get('instance').get('prices')) == stock.prices.count() == len(stock_serializer.data.get('prices'))
        assert set(response.json().get('instance').get('_additional_resources')) == set(stock_serializer.data.get('_additional_resources')) 
    
        

@pytest.mark.django_db
class TestPriceRepresentationModelSerializer:
    def test_fields(self, price_factory):
        price = price_factory()
        serializer_data = PriceRepresentationModelSerializer(price).data
        assert set(serializer_data.keys()) == set(['id', 'price', 'datetime', '_detail'])
        assert serializer_data.get('id') is not None
        assert serializer_data.get('price') is not None
        assert serializer_data.get('datetime') is not None
        assert serializer_data.get('_detail') is not None


@pytest.mark.django_db
class TestPriceModelSerializer:
    def test_fields(self, price_factory):
        stock = price_factory()
        factory = APIRequestFactory()
        request = factory.get("")
        serializer_data = PriceModelSerializer(stock, context= {'request': Request(request)}).data
        assert set(serializer_data.keys()) == set(['id', 'open_price', 'high_price', 'low_price', 'price', 'volume', 'date', 'datetime', 'stock', '_stock'])
        assert set(serializer_data.get('_stock')) ==  set(['id', 'symbol', '_detail'])
        
        assert serializer_data.get('id') is not None
        assert serializer_data.get('open_price') is not None
        assert serializer_data.get('high_price') is not None
        assert serializer_data.get('low_price') is not None
        assert serializer_data.get('price') is not None
        assert serializer_data.get('volume') is not None
        assert serializer_data.get('date') is not None
        assert serializer_data.get('datetime') is not None
        assert serializer_data.get('stock') is not None
        assert serializer_data.get('_stock') is not None

        assert serializer_data.get('_stock').get('id') is not None
        assert serializer_data.get('_stock').get('symbol') is not None
        assert serializer_data.get('_stock').get('_detail') is not None


@pytest.mark.django_db
class TestNbPriceStockModelSerializer:
    def test_fields(self, stock_factory, price_factory):
        stock = stock_factory()
        serializer_data = NbPriceStockModelSerializer(stock).data        
        assert set(serializer_data.keys()) == set(['id', 'symbol', 'nb_prices', 'nb_prices_today', 'prices', '_prices'])
        assert serializer_data.get('id') is not None
        assert serializer_data.get('symbol') is not None
        assert serializer_data.get('nb_prices') is None
        assert serializer_data.get('nb_prices_today') is None
        assert len(serializer_data.get('prices')) == 0
        assert len(serializer_data.get('_prices')) == 0

        price_factory(stock=stock)
        serializer_data = NbPriceStockModelSerializer(stock).data
        assert serializer_data.get('nb_prices') is None
        assert serializer_data.get('nb_prices_today') is None
        assert len(serializer_data.get('prices')) == 1
        assert len(serializer_data.get('_prices')) == 1


class TestMultiplyPricesActionButtonSerializer:
    def test_fields(self):
        serializer_data = MultiplyPricesActionButtonSerializer().data
        assert set(serializer_data.keys()) == set(['number_product'])