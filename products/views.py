from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def all_products(request):
    """ A view to show all products,
    including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show selected product information """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


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

    links = [{'id': 285, 'link': 'products'}]
    """
        {'id': 17, 'link': 'architecture'},
        {'id': 82, 'link': 'castles'},
        {'id': 129, 'link': 'vehicles'},
        {'id': 176, 'link': 'landscapes'},
        {'id': 267, 'link': 'nature'}
    ]"""

    context = {
        'products': products,
        'skus': skus,
        'links': links,
    }
    template = 'products/collections.html'

    return render(request, template, context)
