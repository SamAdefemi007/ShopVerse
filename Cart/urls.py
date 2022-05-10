from django.urls import path, include
from . import views

app_name = "Cart"
urlpatterns = [
    path('', views.cart_detail, name="cart"),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('clear', views.cart_clear, name="cart_clear")
]