from django.test import TestCase
from .forms import UserProfileForm


class TestUserProfileForm(TestCase):
    def test_empty_form_is_valid(self):
        form = UserProfileForm({})
        self.assertTrue(form.is_valid())
