from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile """
    # Get the user profile
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # If the user has submitted a change
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Save the form if valid
            form.save()
            # Display a success message to the user
            messages.success(request, 'Profile updated successfully')
        else:
            # Display an error message if the form is invalid
            messages.error(
                request, 'Update failed. Please check your inputted data.')
    else:
        # Autofill the user profile form with any data saved to the profile
        form = UserProfileForm(instance=profile)

    # Get any orders saved to the profile
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        'email': profile.user.email,
        'full_name': profile.user.get_full_name(),
    }

    # Render the profile template
    return render(request, template, context)


def order_history(request, order_number):
    """ Display the order history for the profile """
    # Collect the order data related to the order number
    order = get_object_or_404(Order, order_number=order_number)

    # Display an info message to the user about it being an old order
    messages.info(request, (
        f'This is an historic confirmation for order number {order_number}.'
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    # Render the order summary for that order
    return render(request, template, context)
