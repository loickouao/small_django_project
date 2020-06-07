import factory

from djangoapp.models import Stock, Price

class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price
        
    stock = factory.SubFactory(StockFactory)


