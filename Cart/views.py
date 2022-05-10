from django.shortcuts import render, get_object_or_404, redirect
from Store.models import Cart, Customer, Products, CartItem
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse


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
    return render(request, 'Cart/cart.html', {'cartitems': cartitems, 'cart': cart, 'quantity': quantity})


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
