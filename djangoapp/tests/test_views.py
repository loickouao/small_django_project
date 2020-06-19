
# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework.response import Response
# from rest_framework import status
# import pytest
# from django.utils import timezone
# from .factories import StockFactory, PriceFactory

# class Test_viewsets(APITestCase):

#     def test_hundred_stock(self):
#         for i in range(100):
#             StockFactory()

#         response = self.client.get(reverse('djangoapp:stock-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 100)

#     def test_stock_IBM(self):
#         stock = StockFactory(symbol='IBM')
#         date = timezone.now()
#         price = PriceFactory(open_price=90.00, high_price=190.00, low_price=20.20, price=100.00, volume=40859, date=date, stock = stock)

#         response = self.client.get(reverse('djangoapp:stock-list'), data={'symbol': stock.symbol})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json()[0].get('symbol'), "IBM")

#         response = self.client.get(reverse('djangoapp:price-list'), data={'stock': stock})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json()[0].get('price'), 100.00)
