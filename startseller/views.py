from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TaxInfoForm, VerifyDetailsForm,ExtendedUserCreationForm,SellerReviewForm,AddProductForm,ProductForm,SellerForm,BusinessInfoForm,StoreInfoForm,ProductInfoForm
from .models import SellerInfo,Category,Seller,Order,SellerProduct,BusinessInfo,StoreInfo,ProductInfo,TaxInfo,VerifyDetails
from products.models import Product
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from django.db.models import Avg 

def signup_view(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            confirm_password = form.cleaned_data['password2']
            
            if password == confirm_password:
                user = form.save(commit=False)
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                login(request, user)
                messages.success(request, 'You have been registered and logged in successfully.')
                return redirect('startseller:home')
            else:
                messages.error(request, 'Passwords do not match. Please enter matching passwords.')
        else:
            messages.error(request, 'Form validation failed. Please check your input.')
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
                return redirect('startseller:home')
            else:
                messages.info(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'startseller/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('startseller:login')

@login_required
def business_info(request):
    business_info, created = BusinessInfo.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = BusinessInfoForm(request.POST, instance=business_info)
        if form.is_valid():
            business_info = form.save(commit=False)
            business_info.user = request.user
            business_info.save()
            return redirect('store_info')
    else:
        form = BusinessInfoForm(instance=business_info)

    return render(request, 'startseller/business_info.html', {'form': form})


@login_required
def store_info(request):
    store_info, created = StoreInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = StoreInfoForm(request.POST, instance=store_info)
        if form.is_valid():
            store_info = form.save(commit=False)
            store_info.user = request.user
            store_info.save()
            return redirect('product_info')
    else:
        form = StoreInfoForm(instance=store_info)

    return render(request, 'startseller/store_info.html', {'form': form})

@login_required
def product_info(request):
    product_info, created = ProductInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProductInfoForm(request.POST, instance=product_info)
        if form.is_valid():
            product_info = form.save(commit=False)
            product_info.user = request.user
            product_info.save()
            return redirect('startseller:tax_info')
    else:
        form = ProductInfoForm(instance=product_info)

    return render(request, 'startseller/product_info.html', {'form': form})


@login_required
def tax_info(request):
    tax_info, created = TaxInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = TaxInfoForm(request.POST, instance=tax_info)
        if form.is_valid():
            tax_info = form.save(commit=False)
            tax_info.user = request.user
            tax_info.save()
            return redirect('startseller:verify_details')
    else:
        form = TaxInfoForm(instance=tax_info)
    return render(request, 'startseller/tax_info.html', {'form': form})


@login_required
def verify_details(request):
    verify_details, created = VerifyDetails.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = VerifyDetailsForm(request.POST, instance=verify_details)
        if form.is_valid():
            verify_details = form.save(commit=False)
            verify_details.user = request.user
            verify_details.save()
            return redirect('startseller:home')
    else:
        form = VerifyDetailsForm(instance=verify_details)
    return render(request, 'startseller/verify_details.html', {'form': form})

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
    
    # Products = SellerProduct.objects.all()
    total_products = SellerProduct.objects.filter(user = request.user).count()
    total_categories = SellerProduct.objects.filter(user = request.user).values('category').distinct().count()
    total_quantity = SellerProduct.objects.filter(user = request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    low_on_stock = SellerProduct.objects.filter(quantity__lte=5, user = request.user).count()
    total_value = SellerProduct.objects.filter(user = request.user).aggregate(total_value=Sum('price'))['total_value']

    # Calculate listings information
    active_listings = SellerProduct.objects.filter(quantity__gt=0,user=request.user).count()
    ready_for_activation = SellerProduct.objects.filter(quantity=0,user=request.user).count()
    inactive_listings = SellerProduct.objects.filter(quantity=0,user=request.user).count()
    out_of_stock = SellerProduct.objects.filter(quantity=0,user=request.user).count()

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
    products = SellerProduct.objects.filter(user=request.user)
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

@login_required
def product_details(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id)
    # reviews = product.reviews.all()
    # average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        form = SellerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('startseller:product_details', product_id=product_id)
    else:
        form = SellerReviewForm()

    context = {
        'product': product,
        # 'reviews': reviews,
        'form': form,
        # 'average_rating': average_rating,
    }
    
    return render(request, 'startseller/product_details.html', context)

@login_required
def update_Product(request, pk):
    product = get_object_or_404(SellerProduct, pk=pk)

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('startseller:seller_product_list')
    else:
        form = AddProductForm(instance=product)

    return render(request, 'startseller/update_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(SellerProduct, pk=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('startseller:all_products')  # Redirect to a different page after deletion

    return render(request, 'startseller/seller_product_list.html', {'product': product})


def list_sellers(request):
    sellers = SellerInfo.objects.all()
    seller_data = [{'name': seller.name,
                    'picture_url': seller.picture.url,
                    'address': seller.address,
                    'contact_details': seller.contact_details} for seller in sellers]
    return render(request, 'startseller/list_sellers.html', {'seller_data': seller_data})
    

@login_required
def seller_detail(request, seller_id):
    seller = SellerInfo.objects.get(id=seller_id)
    # products = seller.product_set.all()  

    context = {
        'seller': seller,
        # 'products': products,
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

# @login_required
def all_sellers(request):
    sellers = SellerInfo.objects.all()

    context = {
        'sellers': sellers,
    }
    return render(request, 'startseller/all_sellers.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('startseller:seller_product_list')
    else:
        form = AddProductForm()

    context = {
        'form': form,
    }
    return render(request, 'startseller/add_product.html', context)

# @login_required
def seller_product_list(request):
    products = SellerProduct.objects.filter(user = request.user)  
    context = {
        'products': products,
    }
    return render(request, 'startseller/seller_product_list.html', context)

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)  
    context = {'order': order}
    return render(request, 'startseller/order_details.html', context)

@login_required
def all_orders(request):
    all_orders = [
        {'order_id': 1, 'status': 'New Order'},
        {'order_id': 2, 'status': 'Urgent'},
        {'order_id': 3, 'status': 'Reached'},
        {'order_id': 4, 'status': 'Reattempted'},
    ]
    return render(request, 'startseller/all_orders.html', {'all_orders': all_orders})

