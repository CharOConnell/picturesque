from django.test import TestCase
from .forms import UserProfileForm


class TestUserProfileForm(TestCase):
    def test_empty_form_is_valid(self):
        form = UserProfileForm({})
        self.assertTrue(form.is_valid())

    def test_fields_are_not_required(self):
        form = UserProfileForm({
            'default_full_name': '',
            'default_email': '',
            'default_phone_number': '',
            'default_street_address1': '',
            'default_street_address2': '',
            'default_town': '',
            'default_county': '',
            'default_postcode': '',
            'default_country': ''})
        self.assertTrue(form.is_valid())
