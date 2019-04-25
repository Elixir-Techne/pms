from __future__ import unicode_literals, absolute_import

from django.urls import path

from . import views

app_name = "masters"

urlpatterns = [
    path('countries', views.get_countries, name='get_countries'),
    path('states', views.get_states, name='get_states'),
    path('cities', views.get_cities, name='get_cities'),
]
