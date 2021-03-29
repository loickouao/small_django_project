# small_django_project

A small Django-Rest Project, that allows to store data for selected stocks.

### Models:
  - Store stocks in a database (Hint: Models → Stock)
  - For each stock, store the prices in the database (Hint: Models → Price with Foreign Key to Stock)
  
### Views:
  - ModelViewSet to retrieve the prices for each stock
  
### Serializers:
  - ModelSerializer to serialize prices from the database into a JSONobject
 
### Tasks:
  - Run a tasks that fetches the prices for a single stock from a remote API
 
 
### APIS:
  - https:////w.alphavantage.co/Python 
  
### Packages:
  - https://pypi.org/project/Django/
  - https://pypi.org/project/djangorestframework/
  - https://pypi.org/project/requests/
  - https://pypi.org/project/celery/ 
  
### (Optional)Helpful Tutorials:
  - https://docs.djangoproject.com/en/3.0/intro/tutorial01/
  - https://w.django-rest-framework.org/tutorial/quickstart/
