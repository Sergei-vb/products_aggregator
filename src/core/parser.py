#!/usr/bin/env python3
import csv


def handle_files(datafile_instance):
    from modules.structure.models import Product, Category, Color, Brand,\
        DataFile

    reader = csv.DictReader(open(datafile_instance.data.path))
    datafile_instance.status = DataFile.BEGIN
    datafile_instance.save(update_fields=['status'])

    necessary_fields = {'Short Description', 'Color', 'Brand', 'Gender',
                        'SubSubcategory', 'Main Category', 'Subcategory'}

    fieldnames_set = set(reader.fieldnames)
    valid_column_names = necessary_fields.issubset(fieldnames_set)

    if not valid_column_names:
        print("error")
        datafile_instance.status = DataFile.ERROR
        datafile_instance.save(update_fields=['status'])

    else:
        for row in reader:
            product_data = {key: '' for key in necessary_fields}

            product_data['Short Description'] = row['Short Description']
            product_data['Gender'] = row['Gender']
            product_data['SubSubcategory'] = row['SubSubcategory']

            product_data['Color'], _ = Color.objects.get_or_create(
                name=row['Color'])

            product_data['Brand'], _ = Brand.objects.get_or_create(
                name=row['Brand'])

            gender_category, _ = Category.objects.get_or_create(
                name=product_data['Gender'], parent=None)

            main_category, _ = Category.objects.get_or_create(
                name=row['Main Category'], parent=gender_category
            )

            product_data['Subcategory'], _ = Category.objects.get_or_create(
                name=row['Subcategory'], parent=main_category
            )

            signal = False

            for val in list(product_data.values()):
                if val is None:
                    signal = True
                    break

            if signal:
                print('error')
                continue

            my_object = Product(name=product_data['Short Description'],
                                color=product_data['Color'],
                                brand=product_data['Brand'],
                                category=product_data['Subcategory'],
                                subcategory=product_data['SubSubcategory'],
                                gender=product_data['Gender'])
            my_object.save()

        datafile_instance.status = DataFile.SUCCESS
        datafile_instance.save(update_fields=['status'])
