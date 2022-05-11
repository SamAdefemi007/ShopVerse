from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Store.models import OrderItem, Products, Customer, Order
from Cart.shoppingCart import Cart
from .forms import CartAddProductForm, PaymentForm
from decimal import Decimal
from django.contrib.auth.decorators import login_required


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


def checkout(request):
    cart = Cart(request)
    return render(request, 'Cart/checkout.html', {'cart': cart})


@login_required
def payments(request):
    cart = Cart(request)
    return render(request, 'Cart/payments.html', {'cart': cart})


def order_complete(request):
    cart = Cart(request)
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.create(payment_status="C", customer=customer)
    order.save()
    for item in cart:
        orderitem = OrderItem.objects.create(
            order=order, product=item['product'], quantity=item['quantity'])

    cart.clear()
    return render(request, 'Cart/order_success.html')
