from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import PositiveIntegerField
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    RoleChoices =(
    ('client', 'client'),
    ('owner', 'owner'),
    ('courier', 'courier'))
    role = models.CharField(max_length=20, choices=RoleChoices, default='client')
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Category(models.Model) :
    category_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.category_name



class Store(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='stores')
    store_name = models.CharField(max_length=30, unique=True)
    store_image = models.ImageField(upload_to='store_photos', null=True, blank=True)
    description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owned_stores')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.store_name


class Contact(models.Model) :
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='contacts')
    contact_name = models.CharField(max_length=20)
    contact_number = PhoneNumberField()

    def __str__(self):
        return f'{self.contact_name}, {self.contact_number}'

class Address(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='addresses')
    address_name = models.CharField(max_length=50)

    def __str__(self):
        return self.address_name


class StoreMenu(models.Model) :
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_menus')
    menu_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.menu_name


class Product(models.Model):
    store = models.ForeignKey(StoreMenu, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='product_photos', null=True, blank=True)
    product_description = models.TextField()
    price = PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.product_name


class Order(models.Model) :
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_client')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    StatusChoices = (
    ('pending', 'pending'),
    ('canceled', 'canceled'),
    ('delivered', 'delivered')
    )
    status = models.CharField(max_length=30, choices=StatusChoices, default='pending')
    delivery_address = models.TextField()
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_courier')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.products}, {self.status}'


class CourierProduct(models.Model) :
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_products')
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='courier_products')
    CourierStatusChoices = (
    ('busy', 'busy'),
    ('available', 'available')
    )
    courier_status = models.CharField(max_length=20, choices=CourierStatusChoices)

    def __str__(self):
        return f'{self.user}. {self.courier_status}'

class Review(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_reviews')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                related_name='courier_reviews', null=True, blank=True)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.rating}'