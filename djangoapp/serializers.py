from bridger import serializers as wb_serializers

from .models import Stock
from .models import Price

class PriceSerializer(wb_serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        depth = 1


class StockSerializer(wb_serializers.ModelSerializer):
    #prices = wb_serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                             view_name='price-detail')
    class Meta:
        model = Stock
        #fields = ['symbol', 'prices']
        fields = '__all__' # all model fields will be included
