from rest_framework import serializers

from .models import Stock
from .models import Price

class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        #fields = ('symbol')
        fields = '__all__' # all model fields will be included

class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
