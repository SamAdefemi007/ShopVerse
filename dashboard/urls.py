from django.urls import path, include
from . import views

app_name = "dashboard"
urlpatterns = [
    path('index/', views.dashboard, name="dashboard"),

]
