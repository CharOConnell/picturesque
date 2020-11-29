from django.test import TestCase
from django.shortcuts import reverse
from products.models import Product


class TestBagViews(TestCase):
    """ Testing on the bag views """

    def test_view_bag(self):
        url = reverse('view_bag')
        response = self.client.get(url)
        # See if it gives us a successful http response
        self.assertEqual(response.status_code, 200)
        # Check the correct template is being used
        self.assertTemplateUsed(response, 'bag/bag.html')

    # def test_add_to_bag(self):
    #     testproduct = Product.objects.create(name='Test Item')
    #     response = self.client.get(f'/add/{testproduct.id}/')
    #     print(testproduct.id, response)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'bag/bag.html')

    # def test_adjust_bag(self):
    #     testproduct = Product.objects.create(name='Test Item')
    #     response = self.client.get(f'/adjust/{testproduct.id}/')
    #     self.assertEqual(response.status_code, 200)
