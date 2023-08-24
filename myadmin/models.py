from django.contrib.auth.models import User
from django.db import models
class MyAdminProduct(models.Model):
    CATEGORY_CHOICES = (
        ('men', 'men'),
        ('women', 'women'),
        ('child', 'child'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(default="This is a good product")
    AdditionalInfo = models.TextField(default="This is a good product")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='men')
    image = models.ImageField(upload_to='product_images/')
    quantity = models.PositiveIntegerField(default=0)  
    def __str__(self):
        return self.name

class MyAdminSellerProduct(models.Model):
    name = models.CharField(max_length=100)
    seller = models.ForeignKey('startseller.Seller', on_delete=models.CASCADE, related_name='myadmin_seller_products_myadmin')  # Use a unique related_name

class MyAdminSellerInfo(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='seller_pics/')
    address = models.TextField()
    contact_details = models.CharField(max_length=100)
