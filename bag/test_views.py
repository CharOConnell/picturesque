from django.test import TestCase
from django.shortcuts import reverse

from products.models import Product


class TestBagViews(TestCase):
    def test_view_bag_page(self):
        url = reverse('view_bag')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_can_add_to_bag(self):
        product = Product.objects.create(name='Test Added Item')
        response = self.client.post(f'/bag/add/{product.id}')
        self.assertEqual(response.get('location'),
                         f'/bag/add/{product.id}/')

    def test_can_adjust_bag(self):
        product = Product.objects.create(name='Test Adjust Item')
        response = self.client.post(f'/bag/adjust/{product.id}')
        self.assertEqual(response.get('location'),
                         f'/bag/adjust/{product.id}/')

    def test_can_remove_from_bag(self):
        product = Product.objects.create(name='Test Removed Item')
        response = self.client.post(f'/bag/remove/{product.id}')
        self.assertEqual(response.get('location'),
                         f'/bag/remove/{product.id}/')
