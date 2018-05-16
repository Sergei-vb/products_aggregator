#!/usr/bin/env python3
from django.urls import path

from .views import Main

urlpatterns = [
    path('', Main.as_view(), name='main'),
]
