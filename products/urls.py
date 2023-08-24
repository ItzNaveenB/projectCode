from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.Home,name="home"),
    path('products/signup/', views.signup_view, name='signup'),
    path('products/login/', views.login_view, name='login'),
    path('products/logout/', views.logout_view, name='logout'),
    path('products/products_list/', views.product_list_view, name='product_list'),
    path('products/product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('products/add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('products/cart/', views.cart, name='cart'),
    path('products/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('products/update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('products/measurements/', views.measurements, name='measurements'),
    path('products/measurement/success/<int:measurement_id>/', views.measurement_success, name='measurement_success'),
    path('products/product/<int:product_id>/add-details/', views.add_details, name='add_details'),
    path('products/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('products/submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

