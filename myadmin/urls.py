from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myadmin'

urlpatterns = [
    path('dashboard/',views.home,name="home"),
    path('catalog/',views.catalog,name="catalog"),
    path('products/', views.Product_list, name='product_list'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('all_sellers/', views.all_sellers, name='all_sellers'),
    path('seller_details/<int:product_id>/',views.seller_details,name="seller_details"),
    path('all_seller_details/', views.all_seller_details, name='all_seller_details'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# {% url 'update_category' category.id %}