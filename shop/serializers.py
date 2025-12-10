from rest_framework import serializers
from .models import (
    User, Address, Category, Product, ProductImage,
    Cart, CartItem, Order, OrderItem
)

# ===============================
# USER SERIALIZER
# ===============================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'name', 'email', 'phone', 'created_at'
        ]


# ===============================
# ADDRESS SERIALIZER
# ===============================
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'address_id', 'user', 'full_name', 'address_line',
            'city', 'state', 'pincode', 'phone'
        ]


# ===============================
# CATEGORY SERIALIZER
# ===============================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name']


# ===============================
# PRODUCT IMAGE SERIALIZER
# ===============================
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image_id', 'image_url']


# ===============================
# PRODUCT SERIALIZER
# ===============================
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(source='productimage_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'product_id', 'name', 'description', 'price', 'discount_price',
            'stock', 'category', 'images'
        ]


# ===============================
# CART ITEM SERIALIZER
# ===============================
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['cart_item_id', 'cart', 'product', 'quantity']


# ===============================
# CART SERIALIZER
# ===============================
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['cart_id', 'user', 'items']


# ===============================
# ORDER ITEM SERIALIZER
# ===============================
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'order_item_id', 'order', 'product',
            'quantity', 'price_at_purchase'
        ]


# ===============================
# ORDER SERIALIZER
# ===============================
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'user', 'address',
            'total_amount', 'status', 'created_at',
            'items'
        ]
