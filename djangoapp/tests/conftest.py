from pytest_factoryboy import register
from .factories import StockFactory, PriceFactory
  
register(StockFactory)
register(PriceFactory)