#!/usr/bin/env python3
from django.views.generic import TemplateView

from .models import Category


class Main(TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


