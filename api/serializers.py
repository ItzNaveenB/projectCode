from rest_framework import serializers
from .models import (
    MyAdminProduct,
    MyAdminSellerInfo,
    Category,
    BusinessInfo,
    StoreInfo,
    ProductInfo,
    TaxInfo,
    VerifyDetails,
    SellerInfo,
    SellerProduct,
    Seller,
    Order,
    SellerReview,
)

class MyAdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAdminProduct
        fields = '__all__'

class MyAdminSellerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAdminSellerInfo
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BusinessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessInfo
        fields = '__all__'

class StoreInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInfo
        fields = '__all__'

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = '__all__'

class TaxInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxInfo
        fields = '__all__'

class VerifyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyDetails
        fields = '__all__'

class SellerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerInfo
        fields = '__all__'

class SellerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProduct
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReview
        fields = '__all__'
