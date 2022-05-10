from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "ShopVerse Staff Dashboard"


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'brand', 'unit_price', 'Rating')
    list_editable = ['unit_price']
    list_filter = ['category', 'brand']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_placed_at', 'payment_status')


@admin.register(Customer)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'phone', 'birth_date')

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'get_customer')

    def get_customer(self, obj):
        return obj.order.customer


admin.site.register(Collection)
admin.site.register(Category)
