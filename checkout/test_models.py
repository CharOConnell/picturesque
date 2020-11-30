from django.test import TestCase
from .models import Order, OrderLineItem
from products.models import Product
from django.conf import settings
from django.db.models import Sum


# from bag.contexts import prices
# import uuid


class TestOrderModel(TestCase):
    def test_order_model_can_create_an_order(self):
        testorder = Order()
        self.assertTrue(testorder)

    def test_generate_order_number_creates_a_new_order(self):
        testorder = Order()
        self.assertFalse(testorder.order_number)
        testorder.order_number = testorder._generate_order_number()
        self.assertTrue(testorder.order_number)


class TestOrderLineItemModel(TestCase):
    def test_string_method_on_line_item_model_returns_sku(self):
        testproduct = Product(sku='test_sku')
        testorder = Order()
        orderlineitem = OrderLineItem(product=testproduct, order=testorder)
        self.assertEqual(
            str(orderlineitem),
            f'SKU {testproduct.sku} on order {testorder.order_number}')
