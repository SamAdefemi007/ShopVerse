import urllib
from urllib.parse import urljoin, urlparse
from behave import given, when, then, model
from django.conf import settings
from django.shortcuts import resolve_url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@given("I navigate to the homepage")
def navigate_to_homepage(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    print(base_url)
    open_url = urljoin(base_url, '/')
    context.browser.get(open_url)


@when("I select the shop now icon")
def select_dropdown(context):
    stepped = context.browser.find_element_by_id('shopping')
    webdriver.ActionChains(context.browser).move_to_element(
        stepped).click(stepped).perform()


@then("I should be able to see products in that category")
def product_added(context):
    print(context.browser.page_source)
    assert 'Search' in context.browser.page_source


@given("I navigate to the products page")
def navigate_to_product(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, '/products')
    print(open_url)
    context.browser.get(open_url)


@when("I click the view product detail icon")
def click_product_detail(context):
    element = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "detail"))
    )
    webdriver.ActionChains(context.browser).move_to_element(
        element).click(element).perform()


@then("I should be able to see the details of the products")
def check_products_spec(context):
    print(context.browser.page_source)
    assert 'Search' in context.browser.page_source
