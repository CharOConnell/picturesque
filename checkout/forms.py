from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """ Create a form format for any orders """
    class Meta:
        """ Give the form fields """
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town', 'county', 'postcode', 'country',)

    def __init__(self, *args, **kwargs):
        """ Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Address Line 1',
            'street_address2': 'Address Line 2',
            'town': 'Town or City',
            'county': 'County',
            'postcode': 'Postcode',
        }

        # Auto focus on the first field
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            # Create placeholders for the fields except country
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Give the form a style for the css
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Disable field labels
            self.fields[field].label = False
