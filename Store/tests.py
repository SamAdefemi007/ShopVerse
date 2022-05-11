from ast import Or
from turtle import title
from typing import Collection
from unicodedata import category
from django.test import TestCase
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from Store.views import homepage, products, productDetail, productSearch, trending, register
from Store.models import Products, Order, OrderItem, Category, Customer, Collection
from django.contrib.auth.models import User
# Create your tests here.

# Testing the urls


class TestUrls(SimpleTestCase):

    def test_homepage_url_resolves(self):
        url = reverse('Store:homepage')
        self.assertEqual(resolve(url).func, homepage)

    def test_products_resolves(self):
        url = reverse('Store:products')
        self.assertEqual(resolve(url).func, products)

    def test_payments_url_resolves(self):
        url = reverse('Store:trending')
        self.assertEqual(resolve(url).func, trending)

    def test_register_url_resolves(self):
        url = reverse('Store:register')
        self.assertEqual(resolve(url).func, register)

    def test_productDetail_url_resolves(self):
        url = reverse('Store:productDetail', kwargs={'product_id': 20})
        self.assertEqual(resolve(url).func, productDetail)

    def test_productsearch_url_resolves(self):
        url = reverse('Store:search')
        self.assertEqual(resolve(url).func, productSearch)

# Testing the views of the application


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.homepage_url = reverse('Store:homepage')
        self.product_url = reverse('Store:products')
        self.productDetail_url = reverse(
            'Store:productDetail', kwargs={'product_id': 20})
        self.search_url = reverse('Store:search')
        self.register_url = reverse('Store:register')

    def test_homepage_GET(self):
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/homepage.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertContains(response, "Women Collection")
        self.assertContains(response, "Girls Collection")
        self.assertContains(response, "Boys Collection")
        self.assertContains(response, "Trending")
        self.assertContains(response, "Shop Now")
        self.assertContains(response, "Subscribe")

    def test_product_GET(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/products.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertContains(response, "Filter by Category")
        self.assertContains(response, "Filter by price")
        self.assertContains(response, "cart")
        self.assertContains(response, "ShopVerse")
        self.assertContains(response, "Sort by")
        self.assertContains(response, "All Price")

    def test_productDetail_GET(self):
        response = self.client.get(self.productDetail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/productdetails.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertContains(response, "cart")

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/register.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'navbar.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertContains(response, "cart")


# Testing Models
class ModelTest(TestCase):

    def setUp(self):
        self.collection = Collection.objects.create(title="clothing")
        self.category = Category.objects.create(title="Men")
        self.user = User.objects.create_user(first_name="django", last_name="test",
                                             email="djangotest@shopverse.com", password='password', username="django_test")
        self.customer = Customer.objects.get(
            user=self.user)
        self.customer.phone = "2342234423",
        self.customer.birth_date = "09/04/201"
        self.product = Products.objects.create(
            size="L", brand="Nike", unit_price=10.00, discounted_price=8.50, image="http://www.google.com", title="Nike sports",
            material="cotton", care="dry wash", color="black", details="Test product", collection=self.collection, category=self.category, style="outdoor", kind="breathable wear", fit="size 6", Rating=4.5)
        self.order = Order.objects.create(
            payment_status="C", customer=self.customer)

    def testCollectionModel(self):
        self.assertEquals(str(self.collection), 'clothing')
        self.assertTrue(isinstance(self.collection, Collection))

    def testCategoryModel(self):
        self.assertEquals(str(self.category), 'Men')
        self.assertTrue(isinstance(self.category, Category))

    def testProductModel(self):

        product = self.product

        self.assertEquals(str(product), 'clothing: Nike sports')
        self.assertTrue(isinstance(product, Products))

    def testCustomerModel(self):
        user = self.user
        customer = self.customer
        customer.phone = "2342234423",
        customer.birth_date = "09/04/201"

        self.assertEquals(str(customer), 'django test')
        self.assertTrue(isinstance(user, User))
        self.assertTrue(isinstance(customer, Customer))

    def testOrderModel(self):
        order = self.order
        self.assertEquals(str(order), 'django test C')
        self.assertTrue(isinstance(order, Order))

    def testOrderItemModel(self):
        orderitem = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=5)
        self.assertEquals(
            str(orderitem), 'clothing: Nike sports by django test C')
        self.assertTrue(isinstance(orderitem, OrderItem))
