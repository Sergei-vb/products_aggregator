from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.ForeignKey(Color, related_name='color_products',
                              on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brand_products',
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category_products',
                                 on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name

