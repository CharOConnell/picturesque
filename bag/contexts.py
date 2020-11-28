from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


prices = {
        'xs': 7.99,
        's': 10.99,
        'm': 12.99,
        'l': 15.99,
        'xl': 18.99,
        'xxl': 20.99,
    }


def bag_contents(request):
    """ Give the bag contents details about the products """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    # Allow for the changeable pricing/sizing on the website
    new_bag_item = []
    new_bag_item_id = []
    new_bag_item_qty = []
    old_bag_item_id = []
    old_bag_item = []
    old_bag_item_qty = []
    new_bag = {}

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        for size, quantity in item_data['items_by_size'].items():
            if '_' in size:
                # The size has been changed
                for item_id, item_data in bag.items():
                    product = get_object_or_404(Product, pk=item_id)
                    for size, quantity in item_data['items_by_size'].items():
                        if '_' not in size:
                            # Get the existing items
                            old_bag_item_id.append(item_id)
                            old_bag_item.append(size)
                            old_bag_item_qty.append(quantity)
                        else:
                            # Split up the updated size
                            old_size = size.split('_')[0]
                            new_size = size.split('_')[1]
                            # Add the new and old items to the new variables
                            new_bag_item_id.append(item_id)
                            new_bag_item.append(new_size)
                            new_bag_item_qty.append(quantity)
                            new_bag_item_id.append(item_id)
                            new_bag_item.append(old_size)
                            new_bag_item_qty.append(-quantity)

                # See if there are any of the size in old bag and remove
                icount = 0
                for old_items in old_bag_item:
                    jcount = 0
                    for new_items in new_bag_item:
                        if (old_items == new_items) & (old_bag_item_id[
                                icount] == new_bag_item_id[jcount]):
                            qty_old = old_bag_item_qty[icount]
                            new_bag_item_qty[jcount] += qty_old
                            old_bag_item_qty[icount] = 0
                        jcount += 1
                    icount += 1

                jcount = 0
                for qty in old_bag_item_qty:
                    if qty <= 0:
                        old_bag_item_qty.remove(old_bag_item_qty[jcount])
                        old_bag_item_id.remove(old_bag_item_id[jcount])
                        old_bag_item.remove(old_bag_item[jcount])
                    jcount += 1

                icount = 0
                for qty in new_bag_item_qty:
                    if qty <= 0:
                        new_bag_item_qty.remove(new_bag_item_qty[icount])
                        new_bag_item_id.remove(new_bag_item_id[icount])
                        new_bag_item.remove(new_bag_item[icount])
                    icount += 1

                # Combine the new and old into one bag
                temp_bag_items = old_bag_item + new_bag_item
                temp_bag_qty = old_bag_item_qty + new_bag_item_qty
                temp_bag_id = old_bag_item_id + new_bag_item_id

                # Create a new id for the bag
                for id in temp_bag_id:
                    new_bag[id] = {'items_by_size': {}}

                # Create the new bag
                icount = 0
                for items in temp_bag_items:
                    if temp_bag_qty[icount] != 0:
                        new_bag[temp_bag_id[icount]][
                            'items_by_size'][items] = temp_bag_qty[icount]
                    icount += 1

                # Reassign the new bag to be the bag
                bag = new_bag

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        for size, quantity in item_data['items_by_size'].items():
            # Add the information to the bag for displaying data
            new_price = Decimal(prices[size])
            product.price = new_price
            total += quantity * product.price
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'product_size': size,
                'product_price': product.price,
            })

    # Calculate the delivery costs
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    # Calculate the order total
    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    # Replace the session variable bag with new one
    request.session['bag'] = bag

    return context
