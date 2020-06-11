from bridger import viewsets
from .serializers import PriceSerializer, StockSerializer
from .models import Stock, Price

# ViewSets define the view behavior.
class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer    

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer