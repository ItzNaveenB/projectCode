from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Product, Cart, CartItem, Measurement,Review
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateCartItemForm, ProductForm, MeasurementForm,ReviewForm,ExtendedUserCreationForm
from django.db.models import Avg

def Home(request):
    return render(request,'products/home.html')

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
            return redirect('product_list')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'products/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have been logged in successfully.')
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def product_list_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        if category == 'topwear':
            products = Product.objects.filter(category='topwear')
        elif category == 'lowerwear':
            products = Product.objects.filter(category='lowerwear')
        else:
            products = Product.objects.all()
    else:
        products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'products/product_list.html', context)

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sizes = ['S', 'M', 'L', 'XL', 'XXL']
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_details', product_id=product_id)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'sizes': sizes,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,
    }
    return render(request, 'products/product_details.html', context)


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    if request.method == 'POST':
        age = request.POST.get('age')
        if int(age) >= 18:
            size = request.POST.get('size')  
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            cart_item.size = size  
            cart_item.save()

            return redirect('cart')
        else:
            messages.error(request, 'You are not eligible to add this product to the cart.')
            return redirect('product_detail', product_id=product.id)

    context = {'product': product}
    return render(request, 'products/product_details.html', context)

@login_required(login_url='login')
def cart(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user, is_paid=False)

    cart_items = CartItem.objects.filter(cart=cart)
    total_cost = sum(item.product.price * item.quantity for item in cart_items)
    measurements = Measurement.objects.filter(user=user)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'measurements_exist': measurements.exists(),
        'measurements': measurements
    }
    return render(request, 'products/cart.html', context)

@login_required(login_url='login')
def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart = get_object_or_404(Cart, user=request.user, is_paid=False)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()

        return HttpResponse(status=200)
    return HttpResponse(status=400)

@login_required(login_url='login')
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == 'POST':
        form = UpdateCartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('cart')
    else:
        form = UpdateCartItemForm(instance=cart_item)

    context = {
        'cart_item': cart_item,
        'form': form
    }
    return render(request, 'products/update_cart_item.html', context)

def measurements(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()

            product_id = measurement.product.id
            return redirect('product_details', product_id=product_id)

    else:
        form = MeasurementForm()

    context = {'form': form}
    return render(request, 'products/measurements.html', context)

def measurement_success(request, measurement_id):
    measurement = get_object_or_404(Measurement, id=measurement_id)
    return render(request, 'products/measurement_success.html', {'measurement': measurement})

@login_required(login_url='login')
def add_details(request, product_id):
    if request.method == 'POST':
        size = request.POST.get('size')
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

        if size in ['S', 'M', 'L', 'XL', 'XXL']:
            # Save the selected size to the cart item
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.size = size
            cart_item.save()

            return redirect('measurements')
        else:
            messages.error(request, 'Invalid size selection.')
            return redirect('product_detail', product_id=product.id)
    return HttpResponse(status=400)

@login_required(login_url='login')
def add_measurement(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = user
            measurement.product = product
            measurement.save()
            return redirect('cart')
    else:
        form = MeasurementForm()

    context = {'product': product, 'form': form}
    return render(request, 'products/measurement.html', context)

@login_required(login_url='login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        if review.user == request.user:
            review.delete()
            messages.success(request, 'Review deleted successfully.')
        else:
            messages.error(request, 'You are not allowed to delete this review.')
    return redirect('product_details',product_id=review.product.id)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReviewForm
from .models import Product

@login_required(login_url='login')
def submit_review(request,product_id):
    # product = get_object_or_404(Product)
    product = Product.objects.get(id = product_id)
    print(product)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully.')
            return redirect('product_details',product_id=product_id)
        else:
            messages.error(request, 'Failed to submit the review. Please check the form data.')
    else:
        form = ReviewForm()

    context = {'form': form, "product_id": product_id}
    # print(product_id)
    return render(request, 'submit_review.html', context)

