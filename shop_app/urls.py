from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('buy_it_now/', views.buy_it_now, name="buy_it_now"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_registration/', views.user_registration, name="user_registration"),
]
