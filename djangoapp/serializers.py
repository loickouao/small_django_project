from bridger import serializers as wb_serializers
from rest_framework.reverse import reverse

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

    @wb_serializers.register_resource()
    def additional_resources(self, instance, request, user):
        additional_resources = dict()
        additional_resources["prices"] = reverse(
            "djangoapp:stock-prices-list",
            args=[instance.id],
            request=request,
        )
        additional_resources["modifyprices"] = reverse(
            "djangoapp:stock-prices-list",
            args=[instance.id],
            request=request,
        )
        return additional_resources

class PriceModelSerializer(wb_serializers.ModelSerializer):
    _stock = StockRepresentationModelSerializer(source="stock")

    class Meta:
        model = Price
        fields = '__all__'
        #depth = 1

