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
    errors = Customer.objects.regi_validator(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)
        return redirect('user_registration')
    else:
        new_customer = Customer.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            date_of_birth=request.POST['date_of_birth'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zipcode=request.POST['zipcode'],
            password=bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt()).decode()

        )

    context = {}
    return render(request, 'user_registration.html', context)


def cart(request):
    context = {}
    return render(request, 'shop_cart.html', context)


def buy_it_now(request):
    context = {}
    return render(request, 'buy_it_now.html', context)
