from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SellerReview,SellerProduct,SellerInfo,BusinessInfo,StoreInfo,ProductInfo,TaxInfo,VerifyDetails

class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

class SellerReviewForm(forms.ModelForm):
    class Meta:
        model = SellerReview
        fields = ['rating', 'comment']

class AddProductForm(forms.ModelForm):
    class Meta:
        model = SellerProduct
        fields = ['name', 'code', 'price', 'quantity', 'max_price','discount', 'image', 'category',]

class SellerForm(forms.ModelForm):
    class Meta:
        model = SellerInfo
        fields = '__all__'
        
class ProductForm(forms.ModelForm):
    seller = forms.ModelChoiceField(queryset=SellerInfo.objects.all(), label='Seller Name')
    
    class Meta:
        model = SellerProduct
        exclude = []  

class BusinessInfoForm(forms.ModelForm):
    class Meta:
        model = BusinessInfo
        fields = ['business_name', 'business_address']

class StoreInfoForm(forms.ModelForm):
    class Meta:
        model = StoreInfo
        fields = ['store_name', 'categories']

class ProductInfoForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ['product_listing', 'shipment_details']

class TaxInfoForm(forms.ModelForm):
    class Meta:
        model = TaxInfo
        fields = ['gst_number', 'bank_account']  

class VerifyDetailsForm(forms.ModelForm):
    class Meta:
        model = VerifyDetails
        fields = ['tax_details', 'signature']  
