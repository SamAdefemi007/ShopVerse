from django.urls import path, include
from . import views

app_name = "Cart"
urlpatterns = [
    path('', views.cart, name="cart"),
]
