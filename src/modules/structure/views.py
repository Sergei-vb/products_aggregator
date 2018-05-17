#!/usr/bin/env python3
from django.views.generic import TemplateView, ListView, DetailView

from .models import Category, Product


class Main(TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ListProducts(ListView):
    template_name = "list_products.html"

    def get_queryset(self):
        queryset = Product.objects.filter(category=self.kwargs['pk'])
        return queryset


class DetailProduct(DetailView):
    template_name = "detail_product.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super(DetailProduct, self).get_context_data(**kwargs)
        context['product'] = Product.objects.get(id=self.kwargs['pk'])
        return context
