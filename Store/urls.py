from django.urls import path, include
from . import views


app_name = "Store"
urlpatterns = [
    path('home/', views.homepage, name="homepage"),
    path('products', views.products, name="products"),
    path('products/<int:product_id>', views.productDetail, name="productDetail"),
    path('register/', views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('carts/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('add_cart/<int:product_id>', views.add_to_cart, name="add_to_cart"),
    path('remove_cart/<int:product_id>',
         views.remove_from_cart, name="remove_from_cart"),

    path('dashboard/', views.dashboard, name="dashboard"),

]
