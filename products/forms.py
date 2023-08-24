from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CartItem, Product, Measurement, Review

class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['id']  

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['product', 'neck', 'chest', 'waist', 'hip', 'inseam']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
