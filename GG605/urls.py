"""GG605 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path

from gg506.views import importshp, runmodel, importda, importhub, importprivate, generatematrixes, calculatephase2, \
    get_da, get_city_connections, get_transit_hubs, get_route, update_da_totalcost, import_cost, app_view, get_cities

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('importshp/', importshp, name="importshp"),
    re_path('importda/', importda, name="importda"),
    re_path('importhub/', importhub, name="importhub"),
    re_path('importprivate/', importprivate, name="importprivate"),
    re_path('generatematrixes/', generatematrixes, name="generatematrixes"),
    re_path('calculatephase2/', calculatephase2, name="calculatephase2"),
    re_path('run/', runmodel, name="runmodel"),
    re_path('getda/', get_da, name="getda"),
    re_path('get_city_connections/', get_city_connections, name="get_city_connections"),
    re_path('get_transit_hubs/', get_transit_hubs, name="get_transit_hubs"),
    re_path('get_route/', get_route, name="get_route"),
    re_path('update_da_totalcost/', update_da_totalcost, name="update_da_totalcost"),
    re_path('import_cost/', import_cost, name="import_cost"),
    re_path('app/',app_view , name="app_view"),
    re_path('get_cities/',get_cities , name="get_cities"),

]
