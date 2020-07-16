"""myapi URL Configuration"""
from django.contrib import admin
from django.urls import path

from . import api_views

urlpatterns = [
    path("400", api_views.error_400),
    path("403", api_views.error_403),
    path("404", api_views.error_404),
    path("404-django", api_views.error_404_django),
    path("500", api_views.error_500),
]
