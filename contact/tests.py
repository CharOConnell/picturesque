from django.test import TestCase
from django.shortcuts import reverse


class TestContactViews(TestCase):
    """ Testing the views in the home app """
    def test_contact_page_view(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    # def test_contact_form_submits(self):
    #     email_post = {'name': 'email_name', 'email': 'email_address_customer', 'subject': 'email_subject', 'message_content': 'email_message'}
    #     response = self.client.post('/contact', email_post)
    #     print(response)
