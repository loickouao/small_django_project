from rest_framework import serializers

from .models import Stock
from .models import Price

class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        depth = 1


class StockSerializer(serializers.HyperlinkedModelSerializer):
    prices = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                 view_name='price-detail')
    class Meta:
        model = Stock
        #fields = ['symbol', 'prices']
        fields = '__all__' # all model fields will be included
