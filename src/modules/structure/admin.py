from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
# from mptt.admin import MPTTModelAdmin

from .models import Category, Product, Brand, Color

# admin.site.register(Genre, MPTTModelAdmin)

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)

admin.site.register(Product)

admin.site.register(Brand)

admin.site.register(Color)
