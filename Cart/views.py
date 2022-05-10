from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Store.models import Products
from Cart.shoppingCart import Cart
from .forms import CartAddProductForm
from decimal import Decimal


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('Cart:cart')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    return redirect('Cart:cart')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('Cart:cart')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True})
        item['get_line_total'] = Decimal(item['price']) * item['quantity']
    print(cart)
    return render(request, 'Cart/cart.html', {'cart': cart})
