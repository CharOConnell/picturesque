from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ Render the shopping bag page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    # Get the product and bag information
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        if size in bag[item_id]['items_by_size'].keys():
            # If that size already exists in the bag, update the quantity
            bag[item_id]['items_by_size'][size] += quantity
            messages.success(request, f'Updated quantity of {size.upper()}\
                {product.name} to {bag[item_id]["items_by_size"][size]}')
        else:
            # The size isn't in the bag so add it
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Added \
                                 {size.upper()} {product.name} to your bag')
    else:
        # That item is not in the bag so add it and its size
        bag[item_id] = {'items_by_size': {size: quantity}}
        messages.success(request, f'Added \
            {size.upper()} {product.name} to your bag')

    # Update the bag variable
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product in the shopping bag """
    # Get the product and bag information
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if quantity > 0:
        # If there are still values of that size, update it to the new quantity
        bag[item_id]['items_by_size'][size] = quantity
        messages.success(request, f'Updated quantity of {size.upper()}\
                {product.name} to {bag[item_id]["items_by_size"][size]}')
    else:
        # If the update removes the size, delete the item from the bag
        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)
        messages.success(request, f'Removed {size.upper()}\
            {product.name} from your bag')

    # Update the bag variable
    request.session['bag'] = bag
    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """ Remove the specified product from the shopping bag """
    try:
        # Get the product and bag information
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST['product_size']
        bag = request.session.get('bag', {})

        # Delete the size and product from the bag
        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:
            bag.pop(item_id)
        messages.success(request, f'Removed {size.upper()}\
            {product.name} from your bag')

        # Update the bag variable
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        # If the item cannot be removed
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
