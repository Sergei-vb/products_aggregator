#!/usr/bin/env python3
from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_genres, name='index'),
]
