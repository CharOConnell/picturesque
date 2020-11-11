from django.http import HttpResponse


class Stripe_WH_Handler:
    """ Handle Stripe webhooks """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle a generic/unknown/unexpeceted webhook event """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
