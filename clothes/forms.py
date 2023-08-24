from django import forms
from .models import Product,UpdateProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = UpdateProduct
        fields = '__all__'
