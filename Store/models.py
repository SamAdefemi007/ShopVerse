import re
from unicodedata import category
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from uuid import uuid4
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Products(models.Model):
    size = models.CharField(max_length=10)
    brand = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField(max_length=2000)
    title = models.CharField(max_length=1000)
    material = models.CharField(max_length=1000)
    care = models.CharField(max_length=5000)
    color = models.CharField(max_length=200)
    details = models.CharField(max_length=5000)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    style = models.CharField(max_length=5000)
    kind = models.CharField(max_length=200)
    fit = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.collection.title}: {self.title}"

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer")
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Customer.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, created, instance, **kwargs):
        try:
            instance.customer.save()
        except ObjectDoesNotExist:
            Customer.objects.create(user=instance)


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed')
    ]

    order_placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.customer} {self.payment_status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Products, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.product} by {self.order}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        cartitems = self.items.all()
        total = 0
        for item in cartitems:
            total += item.calculate_total
        return total

    @property
    def total_items(self):
        cartitems = self.items.all()
        total = 0
        for item in cartitems:
            total += item.quantity
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.cart}- {self.product}"

    @property
    def calculate_total(self):
        total = self.product.unit_price * self.quantity
        return total
