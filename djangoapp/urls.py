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


urlpatterns = [
    path('', include(router.urls)),

]
