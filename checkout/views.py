from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import OrderLineItem, Order

from bag.contexts import bag_contents
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """ Used for the saving data to user page """
    try:
        # Collect the Stripe config variables
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag')),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot\
            be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """ Collect the checkout information """
    # Collect the Stipe config variables
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        # The user has asked to checkout, so collect bag information
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town': request.POST['town'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
            'county': request.POST['county'],
        }

        # Create an order form instance
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # commit=False to stop it saving twice
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                # For each item in the bag
                try:
                    product = Product.objects.get(id=item_id)
                    # Collect the product information
                    for size, quantity in item_data['items_by_size'].items():
                        # Save each item to the order line item model
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_size=size,
                        )
                        order_line_item.save()
                except Product.DoesNotExist:
                    # Product is non existent in database
                    messages.error(request, (
                        "One of the products in your bag was\
                            not found in our database. "
                        "Please call us for assistance."
                    ))
                    # Delete the order
                    order.delete()
                    return redirect(reverse('view_bag'))
            # See if the user has asked to save user information to profile
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                            args=[order.order_number]))
        else:
            # Form entry was invalid
            messages.error(request, "There was an error with your form. \
                Please double check your information.")
    else:
        # Collect the bag information
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request,
                           "There's nothing in your bag at the moment")
            return redirect(reverse('collections'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Prefill the form with any user info saved on the user's profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town': profile.default_town,
                    'county': profile.default_county,
                    'postcode': profile.default_postcode,
                    'country': profile.default_country,
                })
            except UserProfile.DoesNotExist:
                # Render an empty form as no user profile exists
                order_form = OrderForm()
        else:
            # Render an empty form as no user profile exists
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """ Handle successful checkouts """
    # See if the user has requested to save information to profile
    save_info = request.session.get('save_info')
    # Collect order information
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's personal info if checked
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town': order.town,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                # Only save the information if the form is valid
                user_profile_form.save()

    # Let the user know the order has been successful
    messages.success(request, f'Order successfully processed. \
        Your order number is {order_number} and a confirmation email\
            has been sent to {order.email}.')

    # Delete the bag from the session as it has been ordered
    if 'bag' in request.session:
        del request.session['bag']

    # Render the checkout success page with order confirmation details
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
