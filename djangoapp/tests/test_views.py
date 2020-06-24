
from django.urls import reverse
from rest_framework.request import Request
from rest_framework import status
import pytest
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from djangoapp.views import StockRepresentationModelViewSet, StockModelViewSet, PriceRepresentationModelViewSet, PriceModelViewSet, PriceStockModelViewSet
from djangoapp.serializers import MultiplyPricesActionButtonSerializer
from django.contrib.auth import get_user_model
import json

@pytest.mark.django_db      
class TestStockRepresentationViewsets:
    def get_user(self):
        superuser = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )
        return superuser
        
    def test_metadata_list(self, stock_factory):
        for i in range(2):
            stock_factory()
        
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = StockRepresentationModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data 
        assert len(response.data.get('results') ) == 2

    def test_metadata_instance(self, stock_factory):
        stock = stock_factory()
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = StockRepresentationModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=stock.pk)
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.get('instance').keys()) == set(["id", "symbol", "_detail"])
        assert response.data.get('instance').get('id') == stock.id  #Method GET : retrieve a object
        assert response.data.get('instance').get('symbol') == stock.symbol
        assert response.data.get('instance').get('_detail') is not None


@pytest.mark.django_db      
class TestStockViewsets:
    def get_user(self):
        superuser = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )
        return superuser

    def test_metadata_list(self, stock_factory):
        for i in range(2):
            stock_factory()
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        viewset = StockModelViewSet.as_view({"get": "list"})
        response = viewset(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        assert len(response.data.get('results') ) == 2

    def test_metadata_instance(self, stock_factory):
        stock = stock_factory()
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        viewset = StockModelViewSet.as_view({"get": "retrieve"})
        response = viewset(request, pk=stock.pk)
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.get('instance').keys()) == set(["id", "symbol", "prices", "_additional_resources"])
        assert response.data.get('instance').get('id') == stock.id  #Method GET : retrieve a object
        assert response.data.get('instance').get('symbol') == stock.symbol 
        assert len(response.data.get('instance').get('prices')) == stock.prices.count() 
        assert set(response.data.get('instance').get('_additional_resources')) == set(["prices", "modifyprices", "chartprices"])

    
    def test_aggregation(self, stock_factory):
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = StockModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("aggregates") is not None
        assert response.data.get("aggregates").get('symbol').get('#') == '0.00'
        
        for i in range(2):
            stock_factory()
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("aggregates").get('symbol').get('#') == '2.00'


    def test_modifyprices(self, admin_client, stock_factory):
        stock = stock_factory()
        request = APIRequestFactory().get('')
        print(request.POST)
        context = {'request': Request(request)}
        data = {}
        serializers = MultiplyPricesActionButtonSerializer(data = data, context = context)
        assert serializers.is_valid(raise_exception=True)
        assert serializers.data.get('number_product') == 2.0

        data = {
            "number_product" : 3
        }
        serializers = MultiplyPricesActionButtonSerializer(data = data, context = context)
        assert serializers.is_valid()
        assert serializers.data.get('number_product') == 3.0
        response = admin_client.patch(reverse('djangoapp:stock-modifyprices', args=[stock.pk]), data = json.dumps(serializers.data), content_type ='application/json' ) 
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('__notification').get('updated') is True

@pytest.mark.django_db      
class TestPriceRepresentationViewsets:
    def get_user(self):
        superuser = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )
        return superuser
        
    def test_metadata_list(self, stock_factory, price_factory):
        for i in range(2):
            price_factory(stock = stock_factory())
        
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = PriceRepresentationModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data 
        assert len(response.data.get('results') ) == 2

    def test_metadata_instance(self, stock_factory, price_factory):
        stock = stock_factory()
        price = price_factory(stock = stock)
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = PriceRepresentationModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=price.pk)
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.get('instance').keys()) == set(["id", "price", "datetime", "_detail"])
        assert response.data.get('instance').get('id') == price.id  #Method GET : retrieve a object
        assert response.data.get('instance').get('price') == price.price
        assert response.data.get('instance').get('datetime')  == price.datetime.strftime("%Y-%m-%dT%H:%M:%S%z") 
        assert response.data.get('instance').get('_detail') is not None


@pytest.mark.django_db      
class TestPriceViewsets:
    def get_user(self):
        superuser = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )
        return superuser

    def test_metadata_list(self, stock_factory, price_factory):
        for i in range(2):
            price_factory(stock = stock_factory())
        
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = PriceModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data 
        assert len(response.data.get('results') ) == 2

    def test_metadata_instance(self, stock_factory, price_factory):
        stock = stock_factory()
        price = price_factory(stock = stock)
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = PriceModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=price.pk)
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.get('instance').keys()) == set(["id", "open_price", "low_price", "high_price", "price", "volume", "date", "datetime", "stock", "_stock"])
        assert response.data.get('instance').get('id') == price.id  #Method GET : retrieve a object
        assert response.data.get('instance').get('open_price') == price.open_price
        assert response.data.get('instance').get('low_price') == price.low_price
        assert response.data.get('instance').get('high_price') == price.high_price
        assert response.data.get('instance').get('price') == price.price
        assert response.data.get('instance').get('volume') == price.volume
        assert response.data.get('instance').get('date') == price.date.strftime("%Y-%m-%d") 
        assert response.data.get('instance').get('datetime')  == price.datetime.strftime("%Y-%m-%dT%H:%M:%S%z") 
        assert response.data.get('instance').get('stock') == price.stock.id
        assert response.data.get('instance').get('_stock') is not None

    
    def test_aggregation(self, stock_factory, price_factory):
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = PriceModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("aggregates") is not None
        assert response.data.get("aggregates").get('stock').get('#') == '0.00'
        
        for i in range(2):
            price_factory(stock = stock_factory())
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("aggregates").get('stock').get('#') == '2.00'


@pytest.mark.django_db      
class TestPriceStockModelViewSet:
    def get_user(self):
        superuser = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )
        return superuser

    def test_get_list_title(self, admin_client, stock_factory, price_factory):
        stocks = []
        for i in range(2):
            stocks.append(stock_factory())
            price_factory(stock = stocks[i])
        request = APIRequestFactory().get("")
        request.user = self.get_user()
        vs = PriceStockModelViewSet.as_view({"get": "retrieve"}, args=[stocks[0].pk])
        response = vs(request)
        # print(response.data)
        # assert response.status_code == status.HTTP_200_OK
        # assert response.data.get("aggregates") is not None
        

