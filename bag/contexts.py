from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """ Give the bag contents details about the products """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    prices = {
        'xs': 7.99,
        's': 10.99,
        'm': 12.99,
        'l': 15.99,
        'xl': 18.99,
        'xxl': 20.99,
    }

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
                            new_bag_item_qty.append(0)

                # See if there are any of the size in old bag and remove
                jcount = 0
                for qty in new_bag_item_qty:
                    if qty == 0:
                        new_bag_item.remove(new_bag_item[jcount])
                        new_bag_item_qty.remove(new_bag_item_qty[jcount])
                        new_bag_item_id.remove(new_bag_item_id[jcount])
                    jcount += 1

                icount = 0
                for old_item in old_bag_item:
                    for item in new_bag_item:
                        if old_item == item:
                            old_bag_item.remove(old_item)
                            old_bag_item_qty.remove(old_bag_item_qty[icount])
                            old_bag_item_id.remove(old_bag_item_id[icount])
                    icount += 1

                # Create the new bag
                kcount = 0
                for item in old_bag_item:
                    new_bag[old_bag_item_id[kcount]] = {'items_by_size': {}}
                    lcount = 0
                    for new_item in new_bag_item:
                        if old_bag_item_id[kcount] == new_bag_item_id[lcount]:
                            new_bag[old_bag_item_id[kcount]
                                    ]['items_by_size'
                                      ][new_bag_item[lcount]
                                        ] = new_bag_item_qty[lcount]
                            new_bag[old_bag_item_id[kcount]
                                    ]['items_by_size'
                                      ][old_bag_item[kcount]
                                        ] = old_bag_item_qty[kcount]
                    kcount += 1

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
