from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User


class TestProductsViews(TestCase):
    def test_view_bag_page(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_collections_page(self):
        url = reverse('collections')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/collections.html')
