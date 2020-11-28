import uuid

from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile
from bag.contexts import prices


class Order(models.Model):
    """ Create the default model format for an order """
    # Order details
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    date = models.DateTimeField(auto_now_add=True)

    # User information
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=50, null=False, blank=False)
    street_address2 = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(
        blank_label='Country *', null=False, blank=False)

    # Order pricing information
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)

    # Added fields for checking if same order has been placed before
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """ Generate a random, unique order number using UUID, private """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ Update grand total every time a line item is added """
        # Calculate the new order total, allow to be 0 not none if empty
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0

        # Check if the order total is underneath the free delivery threshold
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            # Calculate the delivery cost
            delivery_percentage = Decimal(
                settings.STANDARD_DELIVERY_PERCENTAGE/100)
            self.delivery_cost = self.order_total * delivery_percentage
        else:
            # The delivery is free
            self.delivery_cost = 0

        # Update the total cost with delivery and save
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order
        number if it has not already been set """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        """ Return the order number when called """
        return self.order_number


class OrderLineItem(models.Model):
    """ Create the default model format for each line item in the order """
    order = models.ForeignKey(
        Order, null=False, blank=False,
        on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(
        max_length=3, null=False, blank=False)  # XS, S, M, L, XL, XXL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order
        number if it has not already been set """
        # Update the prices according to size
        self.lineitem_total = prices[self.product_size] * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        """ Return the sku and order number when called """
        return f'SKU {self.product.sku} on order {self.order.order_number}'
