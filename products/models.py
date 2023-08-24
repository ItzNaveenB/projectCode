#products/models.py
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('men', 'men'),
        ('women', 'women'),
        ('child', 'child'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(default="This is a good product")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='men')
    image = models.ImageField(upload_to='product_images/')
    quantity = models.PositiveIntegerField(default=0)  # Track the available quantity of the product

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    age = models.IntegerField(default=0)

    def __str__(self):
        return f"CartItem {self.id} - {self.product.name}"


class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    neck = models.FloatField()
    chest = models.FloatField()
    waist = models.FloatField()
    hip = models.FloatField()
    inseam = models.FloatField()

    def __str__(self):
        return self.user.username + "'s Measurements"

class Review(models.Model):
    RATING_CHOICES = (
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, default='1')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='user_orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    STATUS_CHOICES = (
        ('New Order', 'New Order'),
        ('Urgent', 'Urgent'),
        ('Reached', 'Reached'),
        ('Reattempted', 'Reattempted'),
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"