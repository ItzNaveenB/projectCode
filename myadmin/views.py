from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from startseller.models import SellerInfo ,Seller,SellerProduct, BusinessInfo, StoreInfo, ProductInfo, TaxInfo, VerifyDetails



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

def all_sellers(request):
    sellers = SellerInfo.objects.all()

    context = {
        'sellers': sellers,
    }
    return render(request, 'myadmin/all_sellers.html', context)

def catalog(request):
    username = request.user.username
    products = SellerProduct.objects.all()
    return render(request, 'myadmin/catalog.html', {'products': products})

def Product_list(request):
    print(request.GET.get("category"))
    products = SellerProduct.objects.all()
    
    context = {
        'products': products
    }
    
    return render(request,'myadmin/product_list.html',context)

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