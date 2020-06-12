from bridger import viewsets
from .serializers import (PriceModelSerializer, StockModelSerializer,
    StockRepresentationModelSerializer,
    PriceRepresentationModelSerializer
)
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from django.urls.exceptions import NoReverseMatch

from .models import Stock, Price

from bridger import display as dp

# ViewSets define the view behavior.

class StockRepresentationModelViewSet(viewsets.RepresentationModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockRepresentationModelSerializer


class StockModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = 'djangoapp:stock-list'
    IDENTIFIER = "djangoapp:stock"
    INSTANCE_TITLE = "Stock : {{symbol}}"
    LIST_TITLE = "Stocks"
    CREATE_TITLE = "New Stock"

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="symbol", label="Symbol")
        ],
    )

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=["symbol"]
                )
            )
        ]
    )

    queryset = Stock.objects.all()
    serializer_class = StockModelSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter,]
    ordering_fields = ['symbol']
    ordering = ['symbol']
    search_fields = ("symbol",)


class PriceRepresentationModelViewSet(viewsets.RepresentationModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceRepresentationModelSerializer


class PriceModelViewSet(viewsets.ModelViewSet):

    ENDPOINT = 'djangoapp:price-list'
    IDENTIFIER = 'djangoapp:price' 
    LIST_ENDPOINT = 'djangoapp:pricelist-list'
    INSTANCE_TITLE = "Price : {{price}} / Stock :  {{_stock.symbol}}"
    LIST_TITLE = "Prices"
    CREATE_TITLE = "New Price"
    

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=[
                        dp.FieldSet(fields=["stock"]),
                        dp.FieldSet(fields=["price", "date"]),
                        dp.FieldSet(fields=["open_price", "high_price", "low_price"]),
                        dp.FieldSet(fields=["volume"]),
                    ]
                )
            )
        ]
    )

    queryset = Price.objects.all()
    serializer_class = PriceModelSerializer    

    filter_backends = [filters.OrderingFilter, filters.SearchFilter,]
    ordering_fields = ['stock', 'price', 'date']
    ordering = ['date']
    search_fields = ["stock", "price", "date"]


class PriceListModelViewSet(PriceModelViewSet):
    IDENTIFIER = 'djangoapp:price'
    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="stock", label="Symbol"),
            dp.Field(key="price", label="Price"),
            dp.Field(key="date", label="date"),
        ],  
    )



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_endpoints_root(request, format=None):
    try:
        endpoints = dict()
        for wb_endpoint in settings.WB_ENDPOINTS:
            try:
                endpoints[wb_endpoint] = reverse(
                    f"{wb_endpoint}:api-root", request=request, format=format
                )
            except NoReverseMatch:
                pass

        return Response(endpoints)

    except AttributeError:
        return Response(
            {"error": "No Endpoints specified."}, status=status.HTTP_400_BAD_REQUEST 
        )