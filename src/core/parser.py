#!/usr/bin/env python3
import csv


def handle_files(f):
    from modules.structure.models import Product, Category, Color, Brand

    reader = csv.DictReader(open(f.data.path))
    f.status = 'B'
    f.save(update_fields=['status'])

    try:
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
    except:
        f.status = 'E'
        f.save(update_fields=['status'])
    else:
        f.status = 'S'
        f.save(update_fields=['status'])
