from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.parser import handle_files


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    color = models.ForeignKey(Color, related_name='color_products',
                              on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brand_products',
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category_products',
                                 on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class DataFile(models.Model):
    data = models.FileField()
    all_status = (
        ('N', 'None'),
        ('B', 'Begin'),
        ('S', 'Success'),
        ('E', 'Error'),
    )
    status = models.CharField(max_length=1, choices=all_status, default='N')

    def save(self, *args, **kwargs):
        just_add = self.id is not None
        super(DataFile, self).save(*args, **kwargs)

        if not just_add:
            handle_files(self)
