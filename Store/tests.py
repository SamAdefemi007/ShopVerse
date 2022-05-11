from unicodedata import category
from django.test import TestCase
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from Store.views import homepage, products, productDetail, productSearch, trending, register
# Create your tests here.


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
