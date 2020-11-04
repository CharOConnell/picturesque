from django.shortcuts import render
from .models import Product, Category


def all_products(request):
    """ A view to show all products,
    including sorting and search queries """

    products = Product.objects.all()
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'products/products.html', context)


def collections(request):
    products = Product.objects.all()
    skus = [
        'na100-046',
        'ar010-017',
        'ca020-026',
        've030-016',
        'la060-044',
        'na090-028',
    ]

    context = {
        'products': products,
        'skus': skus,
    }
    template = 'products/collections.html'

    return render(request, template, context)
