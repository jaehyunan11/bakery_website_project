from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.


def store(request):
    customer = Customer.objects.all()
    foods = Food.objects.all()
    # create context to pass some data
    context = {
        'customers': customer,
        'foods': foods,
    }
    return render(request, 'shop_store.html', context)


def user_login(request):
    context = {}
    return render(request, 'user_login.html', context)


def user_registration(request):
    context = {}
    return render(request, 'user_registration.html', context)


def cart(request):
    context = {}
    return render(request, 'shop_cart.html', context)


def buy_it_now(request):
    context = {}
    return render(request, 'buy_it_now.html', context)
