from bridger import viewsets
from .serializers import (PriceModelSerializer, StockModelSerializer,
    StockRepresentationModelSerializer,
    PriceRepresentationModelSerializer,
    NbPriceStockModelSerializer,
    MultiplyPricesActionButtonSerializer
)
from bridger.filters import DjangoFilterBackend
from bridger import buttons as bt
from bridger import display as dp
from bridger.enums import RequestType
from bridger import serializers as wb_serializers
from bridger.notifications.models import Notification, NotificationSendType
from bridger.viewsets import ChartViewSet
from bridger import serializers as wb_serializers
from bridger.pandas.views import PandasAPIView
from bridger.pandas.metadata import PandasMetadata
from bridger.pandas import fields as pf

from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from django.urls.exceptions import NoReverseMatch
from django.db.models import F, Count, Sum, Subquery

from django.utils import timezone
from django.db.models.functions import Coalesce    

import pandas as pd

import plotly.graph_objects as go

from .icons import WBIcon

from .models import Stock, Price
from datetime import timedelta

class StockRepresentationModelViewSet(viewsets.RepresentationModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockRepresentationModelSerializer



class StockModelViewSet(viewsets.ModelViewSet):
    DELETE_ENDPOINT = None
    ENDPOINT = 'djangoapp:stock-list'

    IDENTIFIER = "djangoapp:stock"
    INSTANCE_TITLE = "Stock : {{symbol}}"
    LIST_TITLE = "Stocks"
    CREATE_TITLE = "New Stock"

    LIST_DISPLAY = dp.ListDisplay(
        fields = [
            dp.Field(key = "symbol", label = "Symbol")
        ],
    )

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections = [
            dp.Section(
                fields = dp.FieldSet(
                    fields = ["symbol"]
                )
            ),
            dp.Section(title="Prices", collapsed=True, section_list = dp.SectionList(key = "prices")),
        ]
    )

    CUSTOM_LIST_INSTANCE_BUTTONS = CUSTOM_INSTANCE_BUTTONS = [
        bt.DropDownButton(label="Quick Action", icon = WBIcon.TRIANGLE_DOWN.value, buttons = [

            bt.WidgetButton(key = "prices", label = "Prices", icon = WBIcon.DOLLAR.value),
            
            bt.ActionButton(
                method = RequestType.PATCH,
                identifiers = ["djangoapp:price"],
                action_label = "Modify Prices",
                key = "modifyprices",
                title = "Modify the Prices of a stock",
                label = "Modify Prices",
                icon = WBIcon.CIRCLE_NO.value,
                description_fields = "<p> Do you want to modify the prices of {{symbol}}? </p>",
                serializer = MultiplyPricesActionButtonSerializer,
                confirm_config = bt.ButtonConfig(label = "Confirm"),
                cancel_config = bt.ButtonConfig(label = "Cancel"),
                instance_display = dp.InstanceDisplay(
                    sections=[
                        dp.Section(
                            fields = dp.FieldSet(fields = ["number_product"])
                        )
                    ]
                )
            ),

            bt.WidgetButton(key = "chartprices", label = "Prices Chart", icon = WBIcon.STATS.value),

            bt.HyperlinkButton(endpoint = "https://www.alphavantage.co/", label = "AlphaVantage", icon = WBIcon.BANK.value),


        ])
    ]

    @action(methods = ["PATCH"], permission_classes = [IsAuthenticated], detail=True)
    def modifyprices(self, request, pk = None):
        number_product = float(request.POST.get("number_product", 1))
        nbprice = Price.objects.filter(stock__id=pk).update(price=F('price') * number_product)
        stock = Stock.objects.get(pk = pk)
        #print("Stock: " +str(stock)+ " -> nb of price: " + str(nbprice))
        if nbprice > 0 :
            #print("Stock: " + str(stock) + " -> successful modify stock -> price multiplied by " + str(number_product)) 
            Notification.objects.create(
                title = f'Stock: {stock.symbol} Modify Prices',
                message = f'successful You have multiplied the prices of stock: {stock.symbol} -> price multiplied by ({number_product})',
                send_type = NotificationSendType.SYSTEM.value,
                recipient = request.user
            )
        return Response(
            {"__notification": {stock.symbol: "successful modify stock", 'updated': True, "number_product":number_product}}, status=status.HTTP_200_OK
        )


    queryset = Stock.objects.all()
    serializer_class = StockModelSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['symbol']
    ordering = ['symbol']
    search_fields = ("symbol",)
    filterset_fields = {
        "symbol": ["exact", "icontains"]
    }

    def get_aggregates(self, queryset, **kwargs):
        return {
            "symbol": {"#": format_number(queryset.count())},
        }


class PriceRepresentationModelViewSet(viewsets.RepresentationModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceRepresentationModelSerializer


class PriceModelViewSet(viewsets.ModelViewSet):

    ENDPOINT = 'djangoapp:price-list'
    IDENTIFIER = 'djangoapp:price' 
    INSTANCE_TITLE = "Price : {{price}} / Stock :  {{_stock.symbol}}"
    LIST_TITLE = "Prices"
    CREATE_TITLE = "New Price"
    

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=[
                        dp.FieldSet(fields=["stock"]),
                        dp.FieldSet(fields=["price", "date", "datetime"]),
                        dp.FieldSet(fields=["open_price", "high_price", "low_price"]),
                        dp.FieldSet(fields=["volume"]),
                    ]
                )
            )
        ]
    )

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="stock", label="Symbol"),
            dp.Field(key="price", label="Price"),
            dp.Field(key="date", label="Date"),
            dp.Field(key="datetime", label="Datetime"),
        ],  
    )

    queryset = Price.objects.all()
    serializer_class = PriceModelSerializer    

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['stock', 'price', 'date', 'datetime']
    ordering = ['datetime', 'stock']
    search_fields = ["stock", "price"]
    filterset_fields = {
        "stock": ["exact"],
        "price": ["exact", "icontains"],
        "date": ["gte", "lte"],
        "datetime": ["gte", "lte"]
    }

    def get_aggregates(self, queryset, **kwargs):
        return {
            "stock": {"#": format_number(queryset.count())},
        }

    def get_serializer_changes(self, serializer):
        pk = self.kwargs.get("pk", None)
        if hasattr(serializer, "fields") and pk :
            #if getattr(self.)
            serializer.fields["price"] = wb_serializers.FloatField(read_only=True)
        return serializer


class PriceStockModelViewSet(PriceModelViewSet):
    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="price", label="Price"),
            dp.Field(key="date", label="Date"),
            dp.Field(key="datetime", label="Datetime"),
        ],  
    )
    def get_endpoint(self, request, endpoint=None):
        return "djangoapp:stock-prices-list", [self.kwargs["stock_id"]], {}

    def get_list_title(self, request, field=None):
        stock = Stock.objects.get(id=self.kwargs["stock_id"])
        return f'Prices for {stock.symbol}'

    def get_queryset(self):
        return super().get_queryset().filter(stock__id=self.kwargs["stock_id"])


class PriceStockChartViewSet(ChartViewSet):
    ENDPOINT = 'djangoapp:stock-chartprices-list'
    IDENTIFIER = 'djangoapp:price' 
    queryset = Price.objects.all()
    
    LIST_TITLE = "Model Chart"

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['datetime']
    ordering = ['datetime']
    filterset_fields = {
        "datetime": ["gte", "lte"]
    }

    def get_queryset(self):
        return Price.objects.all().filter(stock__id=self.kwargs["stock_id"])

    def get_list_title(self, request, field=None):
        stock = Stock.objects.get(id=self.kwargs["stock_id"])
        return f'Model Chart - Prices for {stock.symbol}'

    def get_plotly(self, queryset):
        df = pd.DataFrame(
            queryset.order_by("datetime").values("datetime", "price")
        )
        fig = go.Figure([go.Scatter()])
        if not(df.empty):  
            fig = go.Figure(
                [
                    go.Scatter(
                        x = df.datetime,
                        y = df.price,  
                        #mode='lines+markers',
                        #fill='tozeroy',
                        #line = dict(width=1),
                    )
                ]
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(
                    title="Prices",
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    anchor="x",
                    side="right",
                    showline=True,
                    linewidth=1,
                    linecolor="black",
                ),
                yaxis_type="log",
                xaxis=dict(
                    title="Datetime",
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    showline=True,
                    linewidth=0.5,
                    linecolor="black",
                    showgrid=True,
                    gridcolor="lightgray",
                    gridwidth=1,
                ),
                autosize=True,
                xaxis_rangeslider_visible=True,
            )
        return fig


class PricePandasModelViewSet(PandasAPIView):
    ENDPOINT = 'djangoapp:price-list'
    #ENDPOINT = None
    IDENTIFIER = 'djangoapp:price' 
    #LIST_ENDPOINT = 'djangoapp:pricelist-list'
    metadata_class = PandasMetadata

    LIST_TITLE = 'Pandas Prices'

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="stock", label="Symbol"),
            dp.Field(key="price", label="Price"),
            dp.Field(key="date", label="Date"),
            dp.Field(key="datetime", label="Datetime"),
        ],  
    )

    pandas_fields = pf.PandasFields(
        fields=[
            pf.PKField(key="id", label="ID"),
            pf.CharField(key="stock", label="stock"),
            pf.FloatField(key="price", label="Price", precision=2, percent=False),
            pf.CharField(key="date", label="Date"),
            pf.CharField(key="datetime", label="Datetime"),
        ]
    )

    queryset = Price.objects.all()
    serializer_class = PriceModelSerializer 

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['stock', 'price', 'date', 'datetime']
    ordering = ['datetime', 'stock']
    search_fields = ["stock", "price"]
    filterset_fields = {
        "stock": ["exact"],
        "price": ["exact", "icontains"],
        "date": ["gte", "lte"],
        "datetime": ["gte", "lte"]
    }

    def get_aggregates(self, request, df):
        return {
            "stock": {"#": format_number(df.shape[0])},
        }


class NbPriceStockModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = 'djangoapp:price-list'
    IDENTIFIER = 'djangoapp:price' 
    INSTANCE_ENDPOINT = 'djangoapp:stock-list'
    LIST_TITLE = "Nb Stocks"
    
    queryset = Stock.objects.all()
    serializer_class = NbPriceStockModelSerializer 

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="symbol", label="Symbol"),
            dp.Field(key="nb_prices", label="Total Prices"),
            dp.Field(key="nb_prices_today", label="Total Prices today"),
        ],  
    )

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    ordering_fields = ['symbol']
    ordering = ['symbol']
    search_fields = ("symbol",)
    filterset_fields = {
        "symbol": ["exact", "icontains"]
    }

    def get_queryset(self):
        #date = timezone.now().date() - timedelta(days=1)
        today = timezone.now().date()
        return Stock.objects.annotate(
            nb_prices = Count(F("prices")),
            nb_prices_today = Coalesce(Stock.get_nb_prices_stock_date(today), 0)
        )

    def get_aggregates(self, queryset, **kwargs):
        return {
            "symbol": {"#": format_number(queryset.count())},
            "nb_prices": {"#": queryset.aggregate(s=Sum(F("nb_prices")))["s"]},
            "nb_prices_today": {"#": queryset.aggregate(s=Sum(F("nb_prices_today")))["s"]}
        }






















def format_number(number, is_pourcent=False, decimal=2):
    number = number if number else 0
    return f'{number:,.{decimal}{"%" if is_pourcent else "f"}}'


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