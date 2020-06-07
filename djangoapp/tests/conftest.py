from .factories import StockFactory, PriceFactory
from pytest_factoryboy import register

register(StockFactory)
register(PriceFactory)