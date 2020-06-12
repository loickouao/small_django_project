"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from bridger.frontend import FrontendView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from djangoapp.views import api_endpoints_root


urlpatterns = [
    path('admin/', admin.site.urls),

    #FrontendView.bundled_view("frontend/"),
    path("bridger/", include(("bridger.urls", "bridger"), namespace="bridger")),
    FrontendView.bundled_view(""),
    path('', RedirectView.as_view(url=reverse_lazy('frontend'))),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Include all urls for the backend modules
    path('api/', api_endpoints_root, name='base_api_root'),

    path('api/djangoapp/', include(('djangoapp.urls', 'djangoapp'), namespace="djangoapp")),



]
