#!/usr/bin/env python3
import csv

from core.celery import app


@app.task
def handle_files(datafile_id):
    from .models import Product, Category, Color, Brand, DataFile

    datafile_instance = DataFile.objects.get(id=datafile_id)

    reader = csv.DictReader(open(datafile_instance.data.path))
    datafile_instance.status = DataFile.BEGIN
    datafile_instance.save(update_fields=['status'])

    necessary_fields = {'Short Description', 'Color', 'Brand', 'Gender',
                        'SubSubcategory', 'Main Category', 'Subcategory'}

    fieldnames_set = set(reader.fieldnames)
    valid_column_names = necessary_fields.issubset(fieldnames_set)

    if not valid_column_names:
        datafile_instance.logs += 'Error. Wrong column names.\n'
        datafile_instance.status = DataFile.ERROR
        datafile_instance.save(update_fields=['status', 'logs'])

    else:
        counter = 0
        for row in reader:
            product_data = {key: '' for key in necessary_fields}

            product_data['Short Description'] = row['Short Description']
            product_data['Gender'] = row['Gender']
            product_data['Color'] = row['Color']
            product_data['Brand'] = row['Brand']
            product_data['SubSubcategory'] = row['SubSubcategory']
            product_data['Main Category'] = row['Main Category']
            product_data['Subcategory'] = row['Subcategory']

            if not all(product_data.values()):
                counter += 1
                datafile_instance.logs += ('Error. Product didn\'t save. '
                                           'Empty value in the field.\n')
                datafile_instance.save(update_fields=['logs'])
                continue

            product_data['Color'], _ = Color.objects.get_or_create(
                name=product_data['Color'])

            product_data['Brand'], _ = Brand.objects.get_or_create(
                name=product_data['Brand'])

            gender_category, _ = Category.objects.get_or_create(
                name=product_data['Gender'], parent=None)

            product_data['Main Category'], _ = Category.objects.get_or_create(
                name=product_data['Main Category'], parent=gender_category
            )

            product_data['Subcategory'], _ = Category.objects.get_or_create(
                name=product_data['Subcategory'],
                parent=product_data['Main Category']
            )

            my_object = Product(name=product_data['Short Description'],
                                color=product_data['Color'],
                                brand=product_data['Brand'],
                                category=product_data['Subcategory'],
                                subcategory=product_data['SubSubcategory'],
                                gender=product_data['Gender'])
            my_object.save()

        if not counter:
            datafile_instance.status = DataFile.SUCCESS
        else:
            datafile_instance.status = DataFile.ALMOST

        datafile_instance.save(update_fields=['status'])
