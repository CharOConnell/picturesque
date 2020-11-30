from django.test import TestCase
from .models import Product, Category


class TestProductAndCategoryModels(TestCase):
    def test_string_method_returns_product_name(self):
        testproduct = Product(name='test_product')
        self.assertEqual(str(testproduct), 'test_product')

    def test_category_string_method_returns_name(self):
        testcategory = Category(name='test_category')
        self.assertEqual(str(testcategory), 'test_category')

    def test_category_get_friendly_name_returns_friendly_name(self):
        testcategory = Category(name='test_category',
                                friendly_name='test_friendly')
        self.assertEqual(testcategory.get_friendly_name(), 'test_friendly')
