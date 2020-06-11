from django.urls import path, include
from bridger import routers
from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.BridgerRouter()
router.register(r'stocks', views.StockViewSet)
router.register(r'prices', views.PriceViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
