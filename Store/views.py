
from math import prod
from uuid import uuid4
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Collection, Category, Order, OrderItem, Products, Customer
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from uuid import uuid4
from django.core import serializers
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Count
from Cart.forms import CartAddProductForm

from django.db.models import Q

# Create your views here.


def homepage(request):

    return render(request, 'Store/homepage.html')


def products(request):
    productObj = {}
    cart_product_form = CartAddProductForm()
    category_type = request.GET.get("category_type")
    price = request.GET.get("price")
    request.session["category_type"] = category_type
    orderby = request.GET.get('orderby')

    if price:
        if price == "0-25":
            productObj = Products.objects.filter(
                discounted_price__lte=25).order_by('discounted_price')
        elif price == "26-50":
            productObj = Products.objects.filter(
                discounted_price__gt=25).filter(discounted_price__lte=50).order_by('discounted_price')
        elif price == "51-75":
            productObj = Products.objects.filter(
                discounted_price__gt=50).filter(discounted_price__lte=75).order_by('discounted_price')
        else:
            productObj = Products.objects.filter(
                discounted_price__gt=75).order_by('discounted_price')

    elif category_type:
        productObj = Products.objects.filter(
            category__title=category_type)

    else:
        productObj = Products.objects.all()

    if orderby == 'rating':
        productObj = productObj.order_by('-Rating')

    paginator = Paginator(productObj, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Store/products.html', {'page_obj': page_obj, 'category': request.session["category_type"], 'cart_product_form': cart_product_form})


def productDetail(request, product_id):
    cart_product_form = CartAddProductForm()
    productObj = Products.objects.filter(pk=product_id)

    return render(request, 'Store/productdetails.html', {'Products': productObj, 'cart_product_form': cart_product_form})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.customer.phone = form.cleaned_data.get('phone_number')
            user.customer.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('Store:homepage')

    return render(request, 'Store/register.html', {'form': form})


def productSearch(request):
    search_field = request.GET.get("search")
    cart_product_form = CartAddProductForm()

    if search_field:
        productObj = Products.objects.filter(
            Q(title__icontains=search_field) | Q(brand__icontains=search_field))
        paginator = Paginator(productObj, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    return render(request, 'Store/products.html', {'page_obj': page_obj, 'search': search_field, 'cart_product_form': cart_product_form}, )


def trending(request):
    cart_product_form = CartAddProductForm()
    productObj = Products.objects.all().order_by('orderitem')[:100]
    price = request.GET.get("price")
    category_type = request.GET.get("category_type")

    if price:
        if price == "0-25":
            productObj = productObj.objects.filter(
                discounted_price__lte=25).order_by('discounted_price')
        elif price == "26-50":
            productObj = productObj.objects.filter(
                discounted_price__gt=25).filter(discounted_price__lte=50).order_by('discounted_price')
        elif price == "51-75":
            productObj = productObj.objects.filter(
                discounted_price__gt=50).filter(discounted_price__lte=75).order_by('discounted_price')
        else:
            productObj = productObj.objects.filter(
                discounted_price__gt=75).order_by('discounted_price')

    elif category_type:
        productObj = productObj.objects.filter(
            category__title=category_type)
    paginator = Paginator(productObj, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Store/products.html', {'page_obj': page_obj, 'category': request.session["category_type"], 'cart_product_form': cart_product_form})
