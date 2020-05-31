from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=100)

    "method for recognize the different object"
    def __str__(self):
        return self.symbol

class Price(models.Model):
    open_price = models.FloatField() 
    high_price = models.FloatField() 
    low_price = models.FloatField() 
    price = models.FloatField() 
    volume = models.FloatField() 
    date = models.DateTimeField()
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.price)