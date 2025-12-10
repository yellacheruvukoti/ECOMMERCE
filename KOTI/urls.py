from django.contrib import admin
from django.urls import path, include
from shop.views import home

urlpatterns = [
    path('', home),
    path('products/', include('shop.product_urls')),

    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
]
