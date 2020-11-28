from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm
from bag.contexts import prices


def all_products(request):
    """ A view to show all products,
    including sorting and search queries """
    # Collect all the products
    products = Product.objects.all()
    # Reset any existing categories, sorting, or queries
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # If sort is in the request
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                # Sort by name
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                # Sort by category
                sortkey = 'category__name'
            if 'direction' in request.GET:
                # Find the direction
                direction = request.GET['direction']
                if direction == 'desc':
                    # Setup a descending direction
                    sortkey = f'-{sortkey}'
            # Order the products by the sorting key
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            # Filter by category
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            # If a search has been entered
            query = request.GET['q']
            if not query:
                # An empty search was entered
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # Search through the database for any matches in description
            # or name that match the query
            queri = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queri)

    current_sorting = f'{sort}_{direction}'
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    # Render the products page
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show selected product information """
    # Collect the product detail
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'prices': prices
    }

    # Render the product detail page
    return render(request, 'products/product_detail.html', context)


def collections(request):
    """ A view to show the collections page """
    categories = Category.objects.all()
    all_photo = 'P1013936.JPG'

    context = {
        'categories': categories,
        'all': all_photo,
    }
    template = 'products/collections.html'

    # Render the collections page
    return render(request, template, context)


@login_required
def add_product(request):
    """ Add a new product """
    # Display error message to non-superusers
    if not request.user.is_staff:
        messages.error(request, 'Sorry, only the website owner can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        # On submission of the form
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            # If the form is valid, save and display success message to user
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            # Display error message if form is invalid
            messages.error(
                request,
                'Failed to add product.'
                ' Please ensure that your inputs are valid.')
    else:
        # Display an empty form
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    # Render the add product template
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit an existing product """
    # Display error to non-superusers
    if not request.user.is_staff:
        messages.error(request, 'Sorry, only the website owner can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    # Collect the product data
    if request.method == 'POST':
        # On submission of the form, autofill the form with existing data
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # If the form is valid, save and display success message
            form.save()
            messages.success(request, f'Successfully updated {product.name}.')
            # Render the product detail page for that product
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            # Display error message if form is invalid
            aid1 = f'Failed to update {product.name}.'
            aid2 = ' Please ensure inputs are valid.'
            aid = aid1 + aid2
            messages.error(
                request, aid)
    else:
        # Autofill form with existing data
        form = ProductForm(instance=product)
        # Display info message with product name
        messages.info(request, f'You are editing {product.name}.')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    # Render edit product template
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete an existing product """
    # Display error message to non-superusers
    if not request.user.is_staff:
        messages.error(request, 'Sorry, only the website owner can do that.')
        return redirect(reverse('home'))

    # Get product information and delete from database
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    # Display success message on successful delete
    messages.success(request, f'{product.name} has been deleted!')

    # Render the main products template
    return redirect(reverse('products'))
