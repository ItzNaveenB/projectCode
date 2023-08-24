from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    CATEGORY_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('children', 'Children'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

from django.db import models

class UpdateProduct(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    CATEGORY_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('children', 'Children'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
