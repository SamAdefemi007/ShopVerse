import json
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Cart, Collection, Category, Order, OrderItem, Products, Customer, CartItem
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Count
from .dashboard import category_data, brand_data, order_data

# Create your views here.


def homepage(request):
    return render(request, 'store/homepage.html')


def products(request):
    productObj = {}
    category_type = request.GET.get("category_type")
    request.session["category_type"] = category_type

    if category_type:
        productObj = Products.objects.filter(
            category__title=category_type)

    else:
        productObj = Products.objects.all()

    paginator = Paginator(productObj, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/products.html', {'page_obj': page_obj, 'category': request.session["category_type"]})


def productDetail(request, product_id):
    productObj = Products.objects.filter(pk=product_id)
    return render(request, 'store/productdetails.html', {'Products': productObj})


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
            return redirect('homepage')

    return render(request, 'store/register.html', {'form': form})


def cart(request):
    quantity = request.GET.get('quantity')
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cartitems = cart.items.all()
        cartitems.quantity = quantity

    else:
        cartitems = []
        cart = {'get_cart_total': 0, 'total_items': 0}
    print(quantity)
    return render(request, 'store/cart.html', {'cartitems': cartitems, 'cart': cart, 'quantity': quantity})


@login_required
def add_to_cart(request, product_id):
    quantity = request.GET.get('quantity')
    print(quantity)
    product = get_object_or_404(Products, pk=product_id)
    customer = Customer.objects.get(user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cartitem, created = CartItem.objects.get_or_create(
        cart=cart, product=product, quantity=1)
    cart.save()
    cartitem.save()
    category = product.category.title
    return HttpResponseRedirect(reverse('Store:products'))


def remove_from_cart(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    customer = Customer.objects.get(user=request.user)
    cart = get_object_or_404(Cart, customer=customer)
    CartItem.objects.get(cart=cart, product=product).delete()
    return redirect('cart')


def checkout(request):

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cartitems = cart.items.all()
        print(cart.get_cart_total)
    else:
        cartitems = []
        cart = {'get_cart_total': 0, 'total_items': 0}
    return render(request, 'store/checkout.html', {'cartitems': cartitems, 'cart': cart})


def order(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer)
        cartitems = cart.items.all()
        print(cart.get_cart_total)
    else:
        cartitems = []
        cart = {'get_cart_total': 0, 'total_items': 0}
    return render(request, 'store/cart.html', {'cartitems': cartitems, 'cart': cart})


@staff_member_required
def dashboard(request):
    # Render Product segmentation

    category_chart_data = category_data()
    # brands segmentation
    brand_chart_data = brand_data()
    order_chart_data  = order_data()

    print(order_data())
    context = {
        'category_wise_pie_data': json.dumps(category_chart_data),
        'brand_data': json.dumps(brand_chart_data),
        'order_data':json.dumps(order_chart_data)
    }

    return render(request, 'admin_dashboard.html', context)
