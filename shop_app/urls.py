from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('edit_mypage', views.edit_mypage, name="edit_mypage"),
    path('update_mypage', views.update_mypage, name="update_mypage"),
    path('store/', views.store, name="store"),
    path('food_detail/<str:food_name>', views.food_detail, name="food_detail"),
    path('cart/', views.cart, name="cart"),
    path('buy_it_now/', views.buy_it_now, name="buy_it_now"),
    path('update_item/', views.update_item, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]
