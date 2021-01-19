from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
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

    customer = Customer.objects.get(
        id=request.session['customer_id'])
    if customer:
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']

        # create context to pass some data
    foods = Food.objects.all()
    context = {
        'foods': foods,
        'cartItems': cartItems,
        'customers': customer,
    }
    return render(request, 'shop_store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(
            id=request.session['customer_id'])
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'shop_cart.html', context)


def buy_it_now(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(
            id=request.session['customer_id'])
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']
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
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=request.session['customer_id'])
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
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

    else:
        print('user is not logged in')
    return JsonResponse('Payment complete!', safe=False)
