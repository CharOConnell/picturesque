# from django.test import TestCase
# from django.shortcuts import reverse
# from django.contrib.auth.models import User

# from .models import UserProfile
# from .forms import UserProfileForm
# from checkout.models import Order


# class TestProfilesViews(TestCase):
#     """ Testing the views in the profiles app """
#     def test_profile_view(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#         # Template issue
#         self.assertTemplateUsed(response, 'profiles/profile.html')

#     def test_order_history_view(self):
#         order = Order.objects.create()
#         print(order.order_number)
#         #url = reverse('order_history', order.order_number)
#         response = self.client.get(f'order_history/{order.order_number}')
#         #self.assertTemplateUsed(response, 'checkout/checkout_success.html')
#         self.assertEqual(response.status_code, 200)
