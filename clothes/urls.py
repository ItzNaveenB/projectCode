from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    path('success/<int:product_id>/', views.success, name='success'),
    path('list/', views.product_list, name='Product_List'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
