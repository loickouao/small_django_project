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
        fields = ('id', 'price', 'datetime', '_detail')


class StockModelSerializer(wb_serializers.ModelSerializer):
    class Meta:
        model = Stock
        #fields = ['symbol', 'prices']
        #fields = '__all__' # all model fields will be included
        fields = ('id', 'symbol', 'prices', '_additional_resources')

    @wb_serializers.register_resource()
    def additional_resources(self, instance, request, user):
        additional_resources = dict()
        additional_resources["prices"] = reverse(
            "djangoapp:stock-prices-list",
            args=[instance.id],
            request=request,
        )
        additional_resources["modifyprices"] = reverse(
            "djangoapp:stock-modifyprices",
            args=[instance.id],
            request=request,
        )
        additional_resources["chartprices"] = reverse(
            "djangoapp:stock-chartprices-list",
            args=[instance.id],
            request=request,
        )
        return additional_resources


class PriceModelSerializer(wb_serializers.ModelSerializer):
    _stock = StockRepresentationModelSerializer(source="stock")
    class Meta:
        model = Price
        fields = (
            'id',
            "open_price",
            "high_price",
            "low_price",
            "price",
            "volume",
            "date",
            "datetime",
            "stock",
            "_stock"
        )
        #depth = 1


class NbPriceStockModelSerializer(wb_serializers.ModelSerializer):
    _prices = PriceRepresentationModelSerializer(many=True, source="prices")
    nb_prices = wb_serializers.IntegerField(allow_null=True)
    nb_prices_today = wb_serializers.IntegerField(allow_null=True)
    class Meta:
        model = Stock
        fields = ('id',"symbol", "prices", "_prices",  "nb_prices", "nb_prices_today")
        #fields = ('id', "symbol", "nb_prices", "nb_prices_today")

class MultiplyPricesActionButtonSerializer(wb_serializers.Serializer):
        number_product = wb_serializers.FloatField(label="Multiply by", default=2)
        class Meta:
            fields = ("number_product")
