from bridger import serializers as wb_serializers

from .models import Stock, Price

class StockRepresentationModelSerializer(wb_serializers.RepresentationSerializer):

    _detail = wb_serializers.HyperlinkField(reverse_name="djangoapp:stock-detail")

    class Meta:
        model = Stock
        fields = ('id', 'symbol', '_detail')


class PriceRepresentationModelSerializer(wb_serializers.RepresentationSerializer):

    _detail = wb_serializers.HyperlinkField(reverse_name="djangoapp:price-detail")

    class Meta:
        model = Price
        fields = ('id', 'price', 'date', '_detail')



class StockModelSerializer(wb_serializers.ModelSerializer):
    #_prices = PriceRepresentationModelSerializer(many=True, source='prices')
    class Meta:
        model = Stock
        #fields = ['symbol', 'prices']
        fields = '__all__' # all model fields will be included


class PriceModelSerializer(wb_serializers.ModelSerializer):
    _stock = StockRepresentationModelSerializer(source="stock")

    class Meta:
        model = Price
        fields = '__all__'
        #depth = 1

