from django.test import TestCase


class TestHomeViews(TestCase):
    """ Testing the views in the home app """
    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
