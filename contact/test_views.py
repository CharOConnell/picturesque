from django.test import TestCase
from django.shortcuts import reverse
from django.core import mail

import json


class TestContactViews(TestCase):
    """ Testing the views in the home app """
    def test_contact_page_view(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_contact_form_submits_email(self):
        mail.send_mail('Test Email Subject',
                       'test email body',
                       'from@example.com',
                       ['to@example.com'],
                       fail_silently=False)
        # Test that one message has been sent
        self.assertEqual(len(mail.outbox), 1)
        # Verify the subject is correct
        self.assertEqual(mail.outbox[0].
                         subject, 'Test Email Subject')
