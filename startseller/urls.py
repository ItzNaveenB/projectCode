from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'startseller'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('business_info/', views.business_info, name='business_info'),
    path('store_info/', views.store_info, name='store_info'),
    path('product_info/', views.product_info, name='product_info'),
    path('tax_info/', views.tax_info, name='tax_info'),
    path('verify_details/', views.verify_details, name='verify_details'),
    path("home/",views.home,name="home"),
    path('all-orders/', views.all_orders, name='all_orders'),
    path('catalog/', views.catalog, name='catalog'),
    path('add_category/', views.add_category, name='add_category'),
    path('update_category/<int:category_id>/', views.update_category, name='update_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_products/',views.add_product,name="add_product"),
    path('seller_product_list/', views.seller_product_list, name='seller_product_list'),
    path('update_product/<int:pk>/', views.update_Product, name='update_Product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'), 
    path('sellers/<int:seller_id>/', views.seller_detail, name='seller_detail'),
    path('add_seller/', views.add_seller, name='add_seller'),
    path('all_sellers/', views.all_sellers, name='all_sellers'),
    path('product_details/<int:product_id>/',views.product_details,name='product_details'),
    path('toggle-seller/<int:seller_id>/', views.toggle_seller_status, name='toggle_seller_status'),
    path('toggle-product/<int:product_id>/', views.toggle_product_status, name='toggle_product_status'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('order/<int:order_id>/update-delivery-status/', views.update_delivery_status, name='update_delivery_status'),
    path('seller_list/',views.list_sellers,name="list_seller"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
