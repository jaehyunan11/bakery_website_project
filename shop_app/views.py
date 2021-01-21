from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from .utils import cookieCart, cartData, guestOrder
import bcrypt
import json
import datetime

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


def edit_mypage(request):
    context = {
        'customer': Customer.objects.get(id=request.session['customer_id'])
    }
    return render(request, 'edit_mypage.html', context)


def update_mypage(request):
    if request.method == "POST":
        errors = Customer.objects.edit_validator(request.POST)
        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('edit_mypage')
        else:
            customer = Customer.objects.get(id=request.session['customer_id'])
            customer.first_name = request.POST['first_name']
            customer.last_name = request.POST['last_name']
            customer.email = request.POST['email']
            customer.address = request.POST['address']
            customer.city = request.POST['city']
            customer.state = request.POST['state']
            customer.zipcode = request.POST['zipcode']
            customer.password = request.POST['password']
            customer.save()
        return redirect('store')


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    # create context to pass some data
    foods = Food.objects.all()
    context = {
        'foods': foods,
        'cartItems': cartItems,
    }
    return render(request, 'shop_store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'shop_cart.html', context)


def food_detail(request):
    foods = Food.objects.all()
    context = {
        'foods': foods,
    }
    return render(request, 'food_detail.html', context)


def buy_it_now(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'buy_it_now.html', context)


def update_item(request):
    data = json.loads(request.body)
    foodId = data['foodId']
    action = data['action']

    print('Action:', action)
    print('FoodId:', foodId)

    customer = Customer.objects.get(id=request.session['customer_id'])
    food = Food.objects.get(id=foodId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, food=food)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    # Parsing the data and access it
    data = json.loads(request.body)
    # authentication user case
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=request.session['customer_id'])
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    # unauthentication user case (move to utils.py)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transactions_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            # shipping -> shippingInfo -> address,city, state, zipcode
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)
