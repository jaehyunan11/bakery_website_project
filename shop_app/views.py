from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    if not 'customer_id' in request.session:
        return render(request, 'index.html')
    else:
        return redirect('store')


def signup(request):
    if request.method == "GET":
        return redirect('/')
    # Validate Error
    errors = Customer.objects.regi_validator(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
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
        # Restore Customer ID and Customer name in session
        request.session['customer_id'] = new_customer.id
        request.session['customer_name'] = new_customer.first_name
        messages.success(request, "You are successfully registered")
        return redirect('store')


def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = Customer.objects.login_validator(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        customers = Customer.objects.filter(email=request.POST['login_email'])
        if customers:
            customer = customers[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), customer.password.encode()):
                request.session['customer_id'] = customer.id
                request.session['customer_name'] = customer.first_name
                return redirect('store')
            else:
                messages.error(request, "Please check your email/password")
    return redirect('/')


def logout(request):
    request.session.flush()
    messages.success(request, "You are successfully logged out")
    return redirect('/')


def store(request):
    customer = Customer.objects.all()
    foods = Food.objects.all()
    # create context to pass some data
    context = {
        'customers': customer,
        'foods': foods,
    }
    return render(request, 'shop_store.html', context)


def cart(request):
    customer = customer = Customer.objects.get(
        id=request.session['customer_id'])
    if customer:
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'shop_cart.html', context)


def buy_it_now(request):
    if request.user.is_authenticated:
        # customer = request.user.customer
        customer = Customer.objects.get(id=request.session['customer_id'])
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'buy_it_now.html', context)
