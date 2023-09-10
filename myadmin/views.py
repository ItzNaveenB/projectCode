from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from startseller.models import SellerInfo ,Seller,SellerProduct, BusinessInfo, StoreInfo, ProductInfo, TaxInfo, VerifyDetails
from .forms import ExtendedUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

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
                return redirect('myadmin:home')
            else:
                messages.error(request, 'Passwords do not match. Please enter matching passwords.')
        else:
            messages.error(request, 'Form validation failed. Please check your input.')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'myadmin/signup.html', {'form': form})


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
                return redirect('myadmin:home')
            else:
                messages.info(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'myadmin/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def home(request):
    total_sellers = Seller.objects.count()
    active_sellers = Seller.objects.filter(active=True).count()
    inactive_sellers = Seller.objects.filter(active=False).count()

    total_products = SellerProduct.objects.count()  
    active_products = SellerProduct.objects.filter(active=True)
    inactive_stock = SellerProduct.objects.filter(active=False, quantity__gt=0)
    out_of_stock = SellerProduct.objects.filter(active=False, quantity=0)
    low_on_stock = SellerProduct.objects.filter(active=True, quantity__gt=0, quantity__lte=10)

    total_inventory = active_products.count() + inactive_stock.count()
    context = {
        'total_sellers': total_sellers,
        'active_sellers': active_sellers,
        'inactive_sellers': inactive_sellers,
        'total_products': total_products,  
        'active_listings': active_products.count(),
        'inactive_listings': inactive_stock.count(),
        'out_of_stock': out_of_stock.count(),
        'low_on_stock': low_on_stock.count(),
        'total_inventory': total_inventory,
    }
    return render(request, 'myadmin/home.html', context)

# def all_sellers(request):
#     sellers = User.objects.all()

#     context = {
#         'sellers': sellers,
#     }
#     return render(request, 'myadmin/all_sellers.html', context)

def catalog(request):
    
    products = User.objects.all()
    return render(request, 'myadmin/catalog.html', {'products':products})

def Product_list(request):
    print(request.GET.get("category"))
    products = SellerProduct.objects.all()
    
    context = {
        'products': products
    }
    
    return render(request,'myadmin/product_list.html',context)

def all_sellers(request):
    user = request.user
    sellers = User.objects.all()
    seller = sellers.count()
    print(seller)
    business_info = BusinessInfo.objects.filter(user=user)

    context = {
        'sellers': sellers,
        'business_info':business_info
    }
    return render(request, 'myadmin/all_sellers.html', context)

def product_details(request, product_id):
    products = get_object_or_404(SellerProduct, id=product_id)

    context = {
        'product': products,
    }
    return render(request, 'myadmin/product_details.html', context)

def seller_details(request, seller_id):
    seller = SellerInfo.objects.get(id=seller_id)
    products = seller.product_set.all()  

    context = {
        'seller': seller,
        'products': products,
    }
    return render(request, 'myadmin/seller_details.html', context)


def all_seller_details(request):
    user = request.user
    business_info = BusinessInfo.objects.filter(user=user).first()
    store_info = StoreInfo.objects.filter(user=user).first()
    product_info = ProductInfo.objects.filter(user=user).first()
    tax_info = TaxInfo.objects.filter(user=user).first()
    verify_details = VerifyDetails.objects.filter(user=user).first()

    context = {
        'business_info': business_info,
        'store_info': store_info,
        'product_info': product_info,
        'tax_info': tax_info,
        'verify_details': verify_details,
    }

    return render(request, 'myadmin/all_seller_details.html', context)