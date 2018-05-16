#!/usr/bin/env python3
from django.conf.urls import url

from .views import Main, ListProducts

urlpatterns = [
    url(r'^$', Main.as_view(), name='main'),
    url(r'^categories/(?P<pk>\d+)/$',
        ListProducts.as_view(), name='products_list')
]
