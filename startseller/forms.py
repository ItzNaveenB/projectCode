from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SellerReview,SellerProduct,SellerInfo

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
        fields = ['name', 'code', 'price', 'quantity', 'LastPrice', 'image', 'category']

class SellerForm(forms.ModelForm):
    class Meta:
        model = SellerInfo
        fields = '__all__'
        
class ProductForm(forms.ModelForm):
    seller = forms.ModelChoiceField(queryset=SellerInfo.objects.all(), label='Seller Name')
    
    class Meta:
        model = SellerProduct
        exclude = []  