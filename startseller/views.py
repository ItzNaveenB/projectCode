from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ExtendedUserCreationForm,SellerReviewForm,AddProductForm,ProductForm,SellerForm
from .models import BusinessInfo, StoreInfo,SellerInfo, ProductInfo,Category, TaxInfo, VerifyDetails,Seller,Order,SellerProduct
from products.models import Product
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from django.db.models import Avg


def signup_view(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('business_info')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'startseller/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully.')
                return redirect('business_info')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'startseller/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def business_info(request):
    business_info = BusinessInfo.objects.filter(user=request.user).first()
    return render(request, 'startseller/business_info.html', {'business_info': business_info})

def store_info(request):
    store_info = StoreInfo.objects.filter(user=request.user).first()
    return render(request, 'startseller/store_info.html', {'store_info': store_info})

def product_info(request):
    product_info = ProductInfo.objects.filter(user=request.user).first()
    return render(request, 'startseller/product_info.html', {'product_info': product_info})

def tax_info(request):
    tax_info = TaxInfo.objects.filter(user=request.user).first()
    return render(request, 'startseller/tax_info.html', {'tax_info': tax_info})

def verify_details(request):
    verify_details = VerifyDetails.objects.filter(user=request.user).first()
    return render(request, 'startseller/verify_details.html', {'verify_details': verify_details})

@login_required
def toggle_seller_status(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    seller.active = not seller.active  
    seller.save()
    return redirect('startseller:all_sellers')

@login_required
def toggle_product_status(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.active = not product.active  
    product.save()
    return redirect('startseller:seller_product_list')

def update_delivery_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_delivery_status = request.POST['delivery_status']
        order.delivery_status = new_delivery_status
        order.save()
        messages.success(request, 'Delivery status updated successfully.')
        return redirect('startseller:order_details', order_id=order_id)

    return render(request, 'startseller/update_delivery_status.html', {'order': order})

@login_required
def home(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        seller = Seller.objects.create(user=request.user, business_name='Your Business Name', business_address='Your Business Address')
    seller_orders = Order.objects.filter(user=request.user)

    total_products = SellerProduct.objects.count()
    total_categories = SellerProduct.objects.values('category').distinct().count()
    total_quantity = SellerProduct.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    low_on_stock = SellerProduct.objects.filter(quantity__lte=5).count()
    total_value = SellerProduct.objects.aggregate(total_value=Sum('price'))['total_value']

    # Calculate listings information
    active_listings = SellerProduct.objects.filter(quantity__gt=0).count()
    ready_for_activation = SellerProduct.objects.filter(quantity=0).count()
    inactive_listings = SellerProduct.objects.filter(quantity=0).count()
    out_of_stock = SellerProduct.objects.filter(quantity=0).count()

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_quantity': total_quantity,
        'low_on_stock': low_on_stock,
        'total_value': total_value,
        'active_listings': active_listings,
        'ready_for_activation': ready_for_activation,
        'inactive_listings': inactive_listings,
        'out_of_stock': out_of_stock,
    }

    return render(request, 'startseller/Home.html', context)

def catalog(request):
    products = SellerProduct.objects.all()
    return render(request, 'startseller/catalog.html', {'products': products})


def add_category(request):
    categories = Category.objects.all()
    return render(request, 'startseller/add_category.html', {'categories': categories})


def update_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        category_name = request.POST['category_name']
        category_code = request.POST['category_code']
        parent_category_id = request.POST.get('parent_category', None)
        sub_category_id = request.POST.get('sub_category', None)
        category.name = category_name
        category.code = category_code
        
        if parent_category_id:
            category.parent_category_id = parent_category_id
        else:
            category.parent_category = None
        
        if sub_category_id:
            category.sub_category_id = sub_category_id
        else:
            category.sub_category = None

        category.save()

        return redirect('add_category')
    
    return render(request, 'startseller/update_category.html', {'categories': categories, 'category': category})

def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect('add_category')
    
    return render(request, 'startseller/delete_category.html', {'category': category})


def product_details(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id)
    sizes = ['S', 'M', 'L', 'XL', 'XXL']
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        form = SellerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_details', product_id=product_id)
    else:
        form = SellerReviewForm()

    context = {
        'product': product,
        'sizes': sizes,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,
    }
    return render(request, 'startseller/product_details.html', context)


def update_Product(request, pk):
    product = get_object_or_404(SellerProduct, pk=pk)

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('Product_List')
    else:
        form = AddProductForm(instance=product)

    return render(request, 'startseller/update_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(SellerProduct, pk=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('startseller:all_products')  # Redirect to a different page after deletion

    return render(request, 'startseller/seller_product_list.html', {'product': product})

def seller_details(request, seller_id):
    seller = SellerInfo.objects.get(id=seller_id)
    products = seller.product_set.all()  

    context = {
        'seller': seller,
        'products': products,
    }
    return render(request, 'startseller/seller_details.html', context)

def add_seller(request):
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('startseller:all_sellers') 
    else:
        form = SellerForm()
    
    context = {
        'form': form,
    }
    return render(request, 'startseller/add_seller.html', context)

def all_sellers(request):
    sellers = SellerInfo.objects.all()

    context = {
        'sellers': sellers,
    }
    return render(request, 'startseller/all_sellers.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  
            product.save()
            return redirect('startseller:seller_product_list')
    else:
        form = ProductForm()

    context = {
        'form': form,
    }
    return render(request, 'startseller/add_product.html', context)

def seller_product_list(request):
    products = SellerProduct.objects.all()  
    context = {
        'products': products,
    }
    return render(request, 'startseller/seller_product_list.html', context)

def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)  
    context = {'order': order}
    return render(request, 'startseller/order_details.html', context)


def all_orders(request):
    all_orders = [
        {'order_id': 1, 'status': 'New Order'},
        {'order_id': 2, 'status': 'Urgent'},
        {'order_id': 3, 'status': 'Reached'},
        {'order_id': 4, 'status': 'Reattempted'},
    ]
    return render(request, 'startseller/all_orders.html', {'all_orders': all_orders})

