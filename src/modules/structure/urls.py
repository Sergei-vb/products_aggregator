#!/usr/bin/env python3
from django.conf.urls import url

from .views import Main, ListProducts, DetailProduct, ListProductsAll

urlpatterns = [
    url(r'^$', Main.as_view(), name='main'),
    url(r'^categories/(?P<pk>\d+)/$',
        ListProducts.as_view(), name='products_list'),
    url(r'^detail/(?P<pk>\d+)/$',
        DetailProduct.as_view(), name='product_detail'),
    url(r'^categories/all/(?P<pk>\d+)/$',
        ListProductsAll.as_view(), name='products_list_all'),
]
