from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


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
    seller = models.ForeignKey('startseller.Seller', on_delete=models.CASCADE, related_name='myadmin_seller_products_api')  # Use a unique related_name


class MyAdminSellerInfo(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='seller_pics/')
    address = models.TextField()
    contact_details = models.CharField(max_length=100)




class Category(models.Model):
    Parent_Category = (
        ('men','men'),
        ('women','women'),
        ('child','child')
    )
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    parent_category = models.CharField(max_length=20, choices=Parent_Category, default='men')
    sub_category = models.CharField(max_length=20,choices=Parent_Category,default="men")

    def __str__(self):
        return self.name

class BusinessInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='business_infos')  
    business_name = models.CharField(max_length=255, default='')
    business_address = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.business_name

class StoreInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='store_infos')  
    store_name = models.CharField(max_length=255, default='')
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.store_name

class ProductInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='product_infos')  
    product_listing = models.CharField(max_length=255, default='')
    shipment_details = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.product_listing

class TaxInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='tax_infos') 
    gst_number = models.CharField(max_length=255, default='')
    bank_account = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.gst_number

class VerifyDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='verify_details')  
    tax_details = models.CharField(max_length=255, default='')
    signature = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.tax_details


class SellerInfo(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='seller_pics/')
    address = models.TextField()
    contact_details = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class SellerProduct(models.Model):
    CATEGORY_CHOICES = (
        ('men', 'men'),
        ('women', 'women'),
        ('child', 'child'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(default="This is a good product")
    code = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='men')
    image = models.ImageField(upload_to='product_images/',null=True)
    quantity = models.PositiveIntegerField(default=0)
    LastPriceDate = models.DateField(default=now)
    LastPrice = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(SellerInfo, on_delete=models.CASCADE,default=None)
    AdditionalInfo = models.TextField(default="This is a good product")

    def __str__(self):
        return self.name

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_seller')
    business_name = models.CharField(max_length=100)
    business_address = models.TextField()
    categories = models.ManyToManyField(Category, blank=True, related_name='api_seller')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.business_name


class Order(models.Model):
    product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='api_orders')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='api_orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_orders')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    STATUS_CHOICES = (
        ('New Order', 'New Order'),
        ('Urgent', 'Urgent'),
        ('Reached', 'Reached'),
        ('Reattempted', 'Reattempted'),
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    
    DELIVERY_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Failed', 'Failed'),
    )
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='Pending')
      
    def __str__(self):
        return f"Order {self.id} - {self.product.name}"


class SellerReview(models.Model):
    RATING_CHOICES = (
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐'),
    )

    product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='api_seller_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='api_seller_reviews')
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, default='1')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)