from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, UpdateProductForm
from .models import Product, UpdateProduct


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('products:Product_List')
    else:
        form = ProductForm()

    return render(request, 'clothes/add_product.html', {'form': form, 'product': None})


def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:Product_List')  
    else:
        form = UpdateProductForm(instance=product)
    
    return render(request, 'clothes/update_product.html', {'form': form})


def success(request, clothing_id):
    clothing = Product.objects.get(id=clothing_id)
    return render(request, 'clothes/success.html', {'clothing': clothing})


def product_list(request):
    clothing = Product.objects.all()
    return render(request, 'clothes/product_list.html', {'clothing': clothing})
