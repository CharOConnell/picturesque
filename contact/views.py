from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def contact(request):
    """ A view to return the contact page and to submit the contact form """
    # Send an email if the form is submitted
    if request.method == 'POST':
        # Collect the data from the form
        email_name = request.POST['name']
        email_address_customer = request.POST['email']
        email_subject = request.POST['subject']
        email_message = request.POST['message_content']
        # Formulate a body string
        body = f'An e-mail from {email_name}: \n {email_message}'

        # Send an email using Django's send_mail function
        send_mail(
            email_subject,
            body,
            email_address_customer,
            [settings.DEFAULT_FROM_EMAIL]
        )
        # Let the user know an email has successfully been sent
        messages.success(request, f'Thank you {email_name} for your e-mail.')
        # Refresh the page with an empty form
        return redirect(reverse('contact'))
    else:
        # No form submission, render the contact page
        return render(request, 'contact/contact.html')
