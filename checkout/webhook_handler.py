from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time


class Stripe_WH_Handler:
    """ Handle Stripe webhooks """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """ Send an email confirmation to the user """
        # Collect the user email
        customer_email = order.email
        # Collect the predescribed confirmation email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        # Use Django send_mail to send the email to the user
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ Handle the payment_intent.succeeded webhook """
        # Collect the Stripe, bag data
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        # See if the user wanted to save their information
        save_info = intent.metadata.save_info

        # Collect the price data
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                # if there isn't a value, save as None rather than empty
                shipping_details.address[field] = None

        # Update profile information if the user opted to save info
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                line1_addr = shipping_details.address.line1
                profile.default_street_address1 = line1_addr
                line2_addr = shipping_details.address.line2
                profile.default_street_address2 = line2_addr
                profile.default_town = shipping_details.address.city
                profile.default_county = shipping_details.address.state
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_country = shipping_details.address.country
                profile.save()

        # See if the order exists
        order_exists = False
        # Allow for slow processing
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    town__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    postcode__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )  # Using iexact for case insensitivity
                order_exists = True
                # If the order exists, break from the while loop
                break
            except Order.DoesNotExist:
                # Increment the attempt number and wait for a second
                attempt += 1
                time.sleep(1)
        if order_exists:
            # Send confirmation email
            self._send_confirmation_email(order)
            # If it has been set to true as we have an order
            aid1 = f'Webhook received: {event["type"]} | SUCCESS:'
            aid2 = ' Verified order already in database'
            aid = aid1 + aid2
            return HttpResponse(content=aid, status=200)
        else:
            # Reset any existing order data
            order = None
            try:
                # Create a new order
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    town=shipping_details.address.city,
                    county=shipping_details.address.state,
                    postcode=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    for size, quantity in item_data['items_by_size'].items():
                        # Get each line item data
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_size=size,
                        )
                        order_line_item.save()
            except Exception as e:
                if order:
                    # If the order has been created, delete it
                    order.delete()
                return HttpResponse(
                    content=f'Webhoook received: {event["type"]} | ERROR: {e}',
                    status=500)

        # Send confirmation email
        self._send_confirmation_email(order)
        f81 = f'Webhook received: {event["type"]} | SUCCESS:'
        f82 = ' Created order in webhook'
        f8 = f81 + f82
        return HttpResponse(content=f8, status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle a payment_intent.payment_failed webhook """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
