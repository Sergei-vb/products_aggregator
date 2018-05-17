#!/usr/bin/env python3
import csv, sys, os

DIR = '/home/sergei/projects/products_aggregator/src'

DIR2 = '/home/sergei/projects/products_aggregator/src/core'
sys.path.append(DIR)
sys.path.append(DIR2)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_dev'

import django

django.setup()

from modules.structure.models import Product, Category, Color, Brand


def handle_files(f):
    reader = csv.DictReader(open(f))
    for row in reader:
        name = row['Short Description']
        color = Color.objects.get_or_create(name=row['Color'])[0]
        brand = Brand.objects.get_or_create(name=row['Brand'])[0]
        gender = row['Gender']
        subcategory = row['SubSubcategory']

        one = Category.objects.get_or_create(name=gender, parent=None)[0]
        two = Category.objects.get_or_create(
            name=row['Main Category'], parent=one
        )[0]
        three = Category.objects.get_or_create(
            name=row['Subcategory'], parent=two
        )[0]

        my_object = Product(name=name, color=color, brand=brand,
                            category=three, subcategory=subcategory,
                            gender=gender)
        my_object.save()


handle_files('/home/sergei/Downloads/file.csv')
