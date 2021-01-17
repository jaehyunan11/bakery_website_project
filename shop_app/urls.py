from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('buy_it_now/', views.buy_it_now, name="buy_it_now"),
]
