from django.test import TestCase
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from Cart.views import cart_add, cart_clear, cart_remove, cart_detail, checkout, payments, order_complete
# Create your tests here.


class TestUrls(SimpleTestCase):

    def test_cart_add_url_resolves(self):
        url = reverse('Cart:cart')
        self.assertEqual(resolve(url).func, cart_detail)

    def test_checkout_resolves(self):
        url = reverse('Cart:checkout')
        self.assertEqual(resolve(url).func, checkout)

    def test_payments_url_resolves(self):
        url = reverse('Cart:payments')
        self.assertEqual(resolve(url).func, payments)

    def test_ordercomplete_url_resolves(self):
        url = reverse('Cart:order_complete')
        self.assertEqual(resolve(url).func, order_complete)


class TestOtherUrls(TestCase):

    def test_details_url_resolves(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_cart_url_resolves(self):
        client = Client()
        response = client.get('/carts/')
        self.assertEqual(response.status_code, 200)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.cart_url = reverse('Cart:cart')
        self.checkout_url = reverse('Cart:checkout')
        self.payments_url = reverse('Cart:payments')
        self.ordercomplete_url = reverse('Cart:order_complete')

    def test_cart_GET(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Cart/cart.html')
        self.assertContains(response, "Checkout")
        self.assertContains(response, "Cart Summary")
        self.assertContains(response, "Clear Cart")
        self.assertContains(response, "Items")
        self.assertContains(response, "Remove")
        self.assertContains(response, "Quantity")

    def test_checkout_GET(self):
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Cart/checkout.html')
        self.assertContains(response, "Billing Address")

