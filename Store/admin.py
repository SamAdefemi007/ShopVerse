from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "ShopVerse Staff Dashboard"


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'unit_price')


admin.site.register(Collection)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
