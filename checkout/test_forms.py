from django.test import TestCase
from .forms import OrderForm


class TestOrderForm(TestCase):
    def test_full_name_is_required(self):
        form = OrderForm({
            'full_name': '',
            'email': 'test@test.com',
            'phone_number': '0123',
            'street_address1': '1 Somewhere Road',
            'street_address2': 'Another Road',
            'town': 'Some Town',
            'county': 'Berkshire',
            'postcode': 'RG9',
            'country': 'Australia'})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors.keys())
        self.assertEqual(form.errors[
            'full_name'][0], 'This field is required.')

    def test_email_is_required(self):
        form = OrderForm({
            'full_name': 'Test Form',
            'email': '',
            'phone_number': '0123',
            'street_address1': '1 Somewhere Road',
            'street_address2': 'Another Road',
            'town': 'Some Town',
            'county': 'Berkshire',
            'postcode': 'RG9',
            'country': 'Australia'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors[
            'email'][0], 'This field is required.')

    def test_phone_number_is_required(self):
        form = OrderForm({
            'full_name': 'Test Form',
            'email': 'test@test.com',
            'phone_number': '',
            'street_address1': '1 Somewhere Road',
            'street_address2': 'Another Road',
            'town': 'Some Town',
            'county': 'Berkshire',
            'postcode': 'RG9',
            'country': 'Australia'})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors.keys())
        self.assertEqual(form.errors[
            'phone_number'][0], 'This field is required.')

    def test_street_address1_is_required(self):
        form = OrderForm({
            'full_name': 'Test Form',
            'email': 'test@test.com',
            'phone_number': '0123',
            'street_address1': '',
            'street_address2': 'Another Road',
            'town': 'Some Town',
            'county': 'Berkshire',
            'postcode': 'RG9',
            'country': 'Australia'})
        self.assertFalse(form.is_valid())
        self.assertIn('street_address1', form.errors.keys())
        self.assertEqual(form.errors[
            'street_address1'][0], 'This field is required.')

    def test_town_is_required(self):
        form = OrderForm({
            'full_name': 'Test Form',
            'email': 'test@test.com',
            'phone_number': '0123',
            'street_address1': '1 Somewhere Road',
            'street_address2': 'Another Road',
            'town': '',
            'county': 'Berkshire',
            'postcode': 'RG9',
            'country': 'Australia'})
        self.assertFalse(form.is_valid())
        self.assertIn('town', form.errors.keys())
        self.assertEqual(form.errors[
            'town'][0], 'This field is required.')

    def test_country_is_required(self):
        form = OrderForm({
            'full_name': 'Test Form',
            'email': 'test@test.com',
            'phone_number': '0123',
            'street_address1': '1 Somewhere Road',
            'street_address2': 'Another Road',
            'town': 'Some Town',
            'county': 'Berkshire',
            'postcode': 'RG9',
            'country': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors.keys())
        self.assertEqual(form.errors[
            'country'][0], 'This field is required.')

    def test_fields_are_explicit_in_form_metaclass(self):
        form = OrderForm()
        self.assertEqual(form.Meta.fields, (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town', 'county', 'postcode', 'country'))
