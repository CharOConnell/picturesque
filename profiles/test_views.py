from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from .models import UserProfile
from .forms import UserProfileForm


class TestProfilesViews(TestCase):
    """ Testing the views in the profiles app """
    def test_profile_view(self):
        # Requires login
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)
        # Go to the profile page
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_user_profile_form_instantiates_correctly(self):
        # Requires login
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)
        # Go to the profile page
        url = reverse('profile')
        response = self.client.get(url)
        testprofile = UserProfile()
        # Create a userprofile form
        testprofileupdate = UserProfileForm(response, instance=testprofile)
        self.assertTrue(testprofileupdate.is_valid())
