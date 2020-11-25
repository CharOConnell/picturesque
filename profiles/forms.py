from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """ Set up the default user profile form """
    class Meta:
        """ Give the form fields """
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """ Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Address Line 1',
            'default_street_address2': 'Address Line 2',
            'default_town': 'Town or City',
            'default_county': 'County',
            'default_postcode': 'Postcode',
        }

        # Set default auto focus to be on phone number field
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                # For all fields except country
                if self.fields[field].required:
                    # Display placeholder with * if required
                    placeholder = f'{placeholders[field]} *'
                else:
                    # Display placeholder
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Give the fields a class to style from
            self.fields[field].widget.attrs['class'] = 'profile-form-input'
            # Remove labels
            self.fields[field].label = False
