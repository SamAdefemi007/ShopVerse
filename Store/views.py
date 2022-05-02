from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, Collection, Category, Order, OrderItem, Products, Customer, CartItem
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.


def homepage(request):
    collection = Collection.objects.all()
    return render(request, 'store/homepage.html', {'collections': collection})


def products(request):
    productObj = {}
    category_type = request.GET.get("category_type")
    if category_type:
        productObj = Products.objects.filter(
            category__title=category_type)

    paginator = Paginator(productObj, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/products.html', {'page_obj': page_obj, 'category': category_type})


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
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cartitems = cart.items.all()
        print(cart.get_cart_total)
    else:
        cartitems = []
        cart = {'get_cart_total': 0, 'total_items': 0}
    return render(request, 'store/cart.html', {'cartitems': cartitems, 'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    customer = Customer.objects.get(user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cartitem, created = CartItem.objects.get_or_create(
        cart=cart, product=product, quantity=1)
    cart.save()
    cartitem.save()
    return redirect('products')


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
