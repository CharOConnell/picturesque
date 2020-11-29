from django.test import TestCase
from .forms import ProductForm


class TestProductForm(TestCase):
    def test_category_is_required(self):
        form = ProductForm({
            'category': '',
            'sku': 'Product sku',
            'name': 'Product name',
            'description': 'Product description',
            'price': '9.99',
            'image': '1.JPG'})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors.keys())
        self.assertEqual(form.errors[
            'category'][0], 'This field is required.')

    def test_sku_is_required(self):
        form = ProductForm({
            'category': 'Product category',
            'sku': '',
            'name': 'Product name',
            'description': 'Product description',
            'price': '9.99',
            'image': '1.JPG'})
        self.assertFalse(form.is_valid())
        self.assertIn('sku', form.errors.keys())
        self.assertEqual(form.errors[
            'sku'][0], 'This field is required.')

    def test_name_is_required(self):
        form = ProductForm({
            'category': 'Product category',
            'sku': 'Product sku',
            'name': '',
            'description': 'Product description',
            'price': '9.99',
            'image': '1.JPG'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors[
            'name'][0], 'This field is required.')

    def test_description_is_required(self):
        form = ProductForm({
            'category': 'Product category',
            'sku': 'Product sku',
            'name': 'Product name',
            'description': '',
            'price': '9.99',
            'image': '1.JPG'})
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors.keys())
        self.assertEqual(form.errors[
            'description'][0], 'This field is required.')

    def test_price_is_required(self):
        form = ProductForm({
            'category': 'Product category',
            'sku': 'Product sku',
            'name': 'Product name',
            'description': 'Product description',
            'price': '',
            'image': '1.JPG'})
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors[
            'price'][0], 'This field is required.')

    def test_image_is_required(self):
        form = ProductForm({
            'category': 'Product category',
            'sku': 'Product sku',
            'name': 'Product name',
            'description': 'Product description',
            'price': '9.99',
            'image': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors.keys())
        error1 = 'Select a valid choice. That choice is '
        error2 = 'not one of the available choices.'
        errorcode = error1 + error2
        self.assertEqual(form.errors['category'][0], errorcode)

    def test_price_is_a_decimal(self):
        form = ProductForm({
            'category': 'Product category',
            'sku': 'Product sku',
            'name': 'Product name',
            'description': 'Product description',
            'price': 'Test',
            'image': '1.JPG'})
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors[
            'price'][0], 'Enter a number.')

    def test_fields_are_explicit_in_form_metaclass(self):
        form = ProductForm()
        self.assertEqual(form.Meta.fields, '__all__')
