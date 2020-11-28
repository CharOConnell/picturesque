from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    """ Set up the formatting for the product information
    in the admin panel """
    # Fields to display
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'image',
    )

    # Ordering setup
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    """ Set up the formatting for the category information
    in the admin panel """
    # Fields to display
    list_display = (
        'friendly_name',
        'name',
        'image',
    )


# Register the new admin setups
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
