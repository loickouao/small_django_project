import factory

class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "djangoapp.Stock"

class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "djangoapp.Price"
        
    stock = factory.SubFactory(StockFactory)