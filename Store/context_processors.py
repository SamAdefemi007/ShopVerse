from .forms import RegisterForm
from .models import Customer, Cart


def login_form(request):
    return{
        'login_form': RegisterForm()
    }


def totalCart(request):

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cartitems = cart.items.all()
        print(cart.get_cart_total)
    else:
        cartitems = []
        cart = {'get_cart_total': 0, 'total_items': 0}
    count = 0
    for items in cartitems:
        count+=1
    

    return {'cartitems': cartitems, 'cart': cart, 'count':count}
