from django.urls import path, include
from bridger import routers
from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.BridgerRouter()

router.register(r'stocks', views.StockModelViewSet)
router.register(r'stockrepresentation', views.StockRepresentationModelViewSet, basename='stockrepresentation')


router.register(r'prices', views.PriceModelViewSet)
router.register(r'pricerepresentation', views.PriceRepresentationModelViewSet, basename='pricerepresentation')
router.register(r'pricelist', views.PriceListModelViewSet, basename='pricelist')


# Subrouter for the Price of a stock 
price_router = routers.BridgerRouter()
price_router.register(r'prices', views.PriceStockModelViewSet, basename='stock-prices')


urlpatterns = [
    path('', include(router.urls)),
    path('stocks/<int:stock_id>/', include(price_router.urls)),

]
