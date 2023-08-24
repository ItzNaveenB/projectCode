from rest_framework import generics, viewsets
from rest_framework.response import responses
from rest_framework.views import APIView
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
from .serializers import (
    MyAdminProductSerializer,
    MyAdminSellerInfoSerializer,
    CategorySerializer,
    BusinessInfoSerializer,
    StoreInfoSerializer,
    ProductInfoSerializer,
    TaxInfoSerializer,
    VerifyDetailsSerializer,
    SellerInfoSerializer,
    SellerProductSerializer,
    SellerSerializer,
    OrderSerializer,
    SellerReviewSerializer,
)

class MyAdminProductViewSet(viewsets.ModelViewSet):
    queryset = MyAdminProduct.objects.all()
    serializer_class = MyAdminProductSerializer

class MyAdminSellerInfoViewSet(viewsets.ModelViewSet):
    queryset = MyAdminSellerInfo.objects.all()
    serializer_class = MyAdminSellerInfoSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BusinessInfoViewSet(viewsets.ModelViewSet):
    queryset = BusinessInfo.objects.all()
    serializer_class = BusinessInfoSerializer

class StoreInfoViewSet(viewsets.ModelViewSet):
    queryset = StoreInfo.objects.all()
    serializer_class = StoreInfoSerializer

class ProductInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer

class TaxInfoViewSet(viewsets.ModelViewSet):
    queryset = TaxInfo.objects.all()
    serializer_class = TaxInfoSerializer

class VerifyDetailsViewSet(viewsets.ModelViewSet):
    queryset = VerifyDetails.objects.all()
    serializer_class = VerifyDetailsSerializer

class SellerInfoViewSet(viewsets.ModelViewSet):
    queryset = SellerInfo.objects.all()
    serializer_class = SellerInfoSerializer

class SellerProductViewSet(viewsets.ModelViewSet):
    queryset = SellerProduct.objects.all()
    serializer_class = SellerProductSerializer

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class SellerReviewViewSet(viewsets.ModelViewSet):
    queryset = SellerReview.objects.all()
    serializer_class = SellerReviewSerializer
