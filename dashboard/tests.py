from django.test import TestCase
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from dashboard.views import dashboard
# Create your tests here.


class TestUrls(SimpleTestCase):

    def test_dashboard_url_resolves(self):
        url = reverse('dashboard:dashboard')
        self.assertEqual(resolve(url).func, dashboard)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('dashboard:dashboard')
