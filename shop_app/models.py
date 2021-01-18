from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
# Create your models here.


class CustomerManager(models.Manager):
    def regi_validator(self, postdata):
        errors = {}
        # Validate whether first name is less than 2 characters
        if len(postdata['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        # Validate whether first name incldues other than characters
        if len(postdata['first_name']) > 0:
            if not NAME_REGEX.match(postdata['first_name']):
                errors['first_name_format'] = "First name should be only contained characters"
        # Validate whether last name is less than 2 characters
        if len(postdata['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        # Validate whether last name incldues other than characters
        if len(postdata['last_name']) > 0:
            if not NAME_REGEX.match(postdata['last_name']):
                errors['last_name_format'] = "Last name should be only contained characters"
        # Validate whether email is blank
        if len(postdata['email']) < 1:
            errors['email'] = "Please enter your email"
        # Validate whether email is already used in registration
        if len(User.objects.filter(email=postdata['email'])) > 0:
            errors['email'] = "Email already in use"
        # Validate whether email format is correct
        if len(postdata['email']) > 0:
            if not EMAIL_REGEX.match(postdata['email']):
                errors['email_format'] = "Please provide a valid email format"
        # Validate whether password is less than 8 characters
        if len(postdata['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        # Validate whether password is match
        if postdata['password'] != postdata['cf_password']:
            errors['password_not_match'] = "Password does not match"
        # Validate whether birthday field is blank
        if len(postdata['date_of_birth']) < 8:
            errors['date_of_birth'] = "Please enter your birthday"
        # Validate whether user enters valid birthday
        else:
            user_date_of_birth = datetime.strptime(
                postdata['date_of_birth'], "%Y-%m-%d")
            today = datetime.now()
            if user_date_of_birth >= today:
                errors['future_birthday'] = "Birthday cannot be in the future"
        return errors

    def login_validator(self, postdata):
        errors = {}
        # Validate whether login email is blank
        if len(postdata['login_email']) < 1:
            errors['login_email'] = "Please enter your email"
        # Validate whether login email format is correct
        if len(postdata['login_email']) > 0:
            if not EMAIL_REGEX.match(postdata['login_email']):
                errors['email_format'] = "Please provide a valid email format"
        # Validate whether login passoword is blank
        if len(postdata['login_password']) < 1:
            errors['login_password'] = "Please enter your password"
        # Filter login user
        customers = Customer.objects.filter(email=postdata['login_email'])
        # Validate whether user signs up email.
        if len(postdata['login_email']) > 0:
            if not customers:
                errors['login_email'] = "Your email has not been signed up!"
        return errors


class Customer(models.Model):
    # User can have one customer and customer can have one user.
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField()
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Food(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    # models.SET_NULL means order will be remained although customer is deleted.
    # customer vs Order (customer can have multiple orders)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    food = models.ForeignKey(
        Food, on_delete=models.SET_NULL, blank=True, null=True)
    # cart can have multiple ordertiems
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food.name

    @property
    def get_total(self):
        total = self.food.price * self.quantity
        return total


class ShippingAddress(models.Model):
    # just in case if order is deleted
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.address
