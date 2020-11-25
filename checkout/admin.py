from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """ Create an inline table for the line item in the admin panel """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """ Create a table for the full order in the admin panel """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date', 'delivery_cost',
                       'order_total', 'grand_total', 'original_bag',
                       'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name', 'email',
              'phone_number', 'street_address1', 'street_address2',
              'town', 'county', 'postcode', 'country',
              'delivery_cost', 'order_total', 'grand_total',
              'original_bag', 'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost', 'grand_total',)

    ordering = ('-date',)


# Register the admin to the site
admin.site.register(Order, OrderAdmin)
