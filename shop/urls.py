from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appname.views import products_page  # your HTML page view
from appname.viewsets import (
    UserViewSet, CategoryViewSet, ProductViewSet,
    CartViewSet, OrderViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),     # Your API routes
    path('products-page/', products_page),  # Your HTML page
]
