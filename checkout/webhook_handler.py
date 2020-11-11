from django.http import HttpResponse


class Stripe_WH_Handler:
    """ Handle Stripe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ Handle the payment_intent.succeeded webhook """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.data.charges[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
                # if there isn't a value, save as None rather than empty

        # see if the order exists
        order_exists = False
        # allow for slow processing
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=shipping_details.email,
                    phone_number__iexact=shipping_details.phone,
                    street_address1__iexact=shipping_details.line1,
                    street_address2__iexact=shipping_details.line2,
                    town__iexact=shipping_details.city,
                    county__iexact=shipping_details.state,
                    postcode__iexact=shipping_details.postal_code,
                    country__iexact=shipping_details.country,
                    grand_total=grand_total,
                )  # use iexact for case insensitivity
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            # if it has been set to true as we have an order
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified order already in database',
                status=200)
        else:
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=shipping_details.email,
                    phone_number=shipping_details.phone,
                    street_address1=shipping_details.line1,
                    street_address2=shipping_details.line2,
                    town=shipping_details.city,
                    county=shipping_details.state,
                    postcode=shipping_details.postal_code,
                    country=shipping_details.country,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    for size, quantity in item_data['items_by_size'].items():
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_size=size,
                        )
                        order_line_item.save()
            except Exception as e:
                if order:
                    order.delete() # delete if created
                return HttpResponse(
                    content=f'Webhoook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle a payment_intent.payment_failed webhook """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
