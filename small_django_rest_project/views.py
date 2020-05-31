from django.shortcuts import render
from rest_framework import viewsets
from .serialize import PriceSerializer, StockSerializer
from .models import Stock, Price
#from .tasks import add, global_quote_celery
import requests
# Create your views here.

# ViewSets define the view behavior.
class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer    
    # celery
    #global_quote_celery()
    #add.apply_async(1,1) #error type
    #add.delay(1,1) #stacks forever

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer    

   


   
   
