"""
URL configuration for drf_cauth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import re_path as url, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import urls as drf_urls
from app_api.views import CountryListView, AuthAPIView, AuthLogoutAPIView

admin.site.site_header = "Countries API Admin"
admin.site.site_title = "Countries API Admin"
admin.site.index_title = "Countries API Admin"


schema_view = get_schema_view(
   openapi.Info(
      title="Countries around the world",
      default_version='v1',
      description="POC: Sample API that implements DRF expiring access tokens",
      license=openapi.License(
          name="The MIT License Copyright 2024 - João de Carvalho"),
   ),
   public=False,
)

api_patterns = [
    url(r'^countries/$', CountryListView.as_view(), name='countries'),
]

urlpatterns = [
    url(r'^auth/login/', include(drf_urls)),
    url(r'^auth/rest/login/$', AuthAPIView.as_view(), name='authentication'),
    url(r'^auth/rest/logout/$', AuthLogoutAPIView.as_view(), name='logout'),
    url(r'^(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^$', schema_view.with_ui('swagger',cache_timeout=0), name='docs'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(api_patterns)),
]
