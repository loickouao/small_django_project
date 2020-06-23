from django.db import models
from django.db.models import F, OuterRef, Count, Subquery, IntegerField

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=100)

    # method for recognize the different object
    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    @classmethod
    def get_representation_endpoint(cls):
        return "djangoapp:stockrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{symbol}}"


    @classmethod
    def get_nb_prices_stock_date(cls, date=None):
        myprices = Price.objects.filter(
            stock__pk = OuterRef('pk'),
            date__gte = date,
        )     
        nb_prices_today = Subquery(
            myprices.values("stock__pk").annotate(count=Count("stock__pk"))
            .values("count")[:1]
            )
        return nb_prices_today

        



class Price(models.Model):
    open_price = models.FloatField(null=False, blank=False) 
    high_price = models.FloatField(null=False, blank=False) 
    low_price = models.FloatField(null=False, blank=False) 
    price = models.FloatField(null=False, blank=False) 
    volume = models.IntegerField(null=False, blank=False) 
    date = models.DateField(auto_now=True)
    datetime = models.DateTimeField(auto_now=True)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='prices')

    def __str__(self):
        return str(self.price)

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"

    @classmethod
    def get_representation_endpoint(cls):
        return "djangoapp:pricerepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{price}}"
