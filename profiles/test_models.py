from django.test import TestCase
from .models import UserProfile
from django.contrib.auth.models import User


class TestProductModels(TestCase):
    def test_profile_can_create_an_order(self):
        profile = UserProfile()
        self.assertTrue(profile)

    def test_create_or_update_user_profile(self):
        testuser = User.objects.create(username='testusername')
        self.assertEqual(str(testuser), 'testusername')

    def test_string_method_returns_username(self):
        testuser = User.objects.create(username='testusername')
        testprofile = UserProfile.objects.get(user=testuser)
        self.assertEqual(str(testprofile), 'testusername')
