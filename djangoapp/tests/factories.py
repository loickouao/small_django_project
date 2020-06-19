import factory
import pytz
from django.conf import settings
from faker import Faker

class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "djangoapp.Stock"

    symbol = factory.Faker("pystr", min_chars=  3, max_chars = 20)


class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "djangoapp.Price"
    
    open_price = factory.Faker("pyfloat", min_value = 0, right_digits=2)
    high_price = factory.Faker("pyfloat", min_value = 0, right_digits=2)
    low_price = factory.Faker("pyfloat", min_value = 0, right_digits=2)
    price = factory.Faker("pyfloat", min_value = 0, right_digits=2)
    volume = factory.Faker("pyint", min_value = 1, max_value = 100000)
    date = factory.Faker("date_object")
    datetime = pytz.timezone(settings.TIME_ZONE).localize(Faker().date_time())
    #datetime = pytz.timezone(settings.TIME_ZONE).localize(factory.Faker('date_time'))
    stock = factory.SubFactory(StockFactory)

