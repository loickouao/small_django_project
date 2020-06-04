import factory

from .models import Stock, Price

class StockFactory(factory.DjangoModelFactory):
    class Meta:
        model = Stock


class PriceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Price
        
    stock = factory.SubFactory(StockFactory)