from django.urls import path, include
from . import views


app_name = "Store"
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('products', views.products, name="products"),
    path('products/<int:product_id>', views.productDetail, name="productDetail"),
    path('register/', views.register, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('checkout/', views.checkout, name="checkout"),
    path('search/', views.productSearch, name="search")

]
