from django.db import models

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


    # @classmethod
    # def 

class Price(models.Model):
    open_price = models.FloatField(null=False, blank=False) 
    high_price = models.FloatField(null=False, blank=False) 
    low_price = models.FloatField(null=False, blank=False) 
    price = models.FloatField(null=False, blank=False) 
    volume = models.FloatField(null=False, blank=False) 
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
