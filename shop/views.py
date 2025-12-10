from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
import requests


def home(request):
    try:
        response = requests.get("http://127.0.0.1:8000/api/products/")
        products = response.json()
    except:
        products = []  # if API down or no product

    return render(request, "home.html", {"products": products})
def products_page(request):
    # Fetch products from your API
    try:
        response = requests.get("http://127.0.0.1:8000/api/products/")
        products = response.json()
    except:
        products = []

    return render(request, "products.html", {"products": products})


from .models import (
    User, Category, Product, ProductImage,
    Cart, CartItem, Order, OrderItem, Address
)

from .serializers import (
    UserSerializer, CategorySerializer, ProductSerializer,
    CartSerializer, CartItemSerializer,
    OrderSerializer, AddressSerializer
)


# ==============================================================
#   USER REGISTRATION API
# ==============================================================
class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        phone = request.data.get('phone')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=400)

        user = User.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone
        )

        return Response({'message': 'User registered successfully', 'user_id': user.user_id})


    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email, password=password)
            return Response({'message': 'Login successful', 'user_id': user.user_id})
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=400)



# ==============================================================
#   CATEGORY VIEWSET (GET ONLY)
# ==============================================================
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



# ==============================================================
#   PRODUCT VIEWSET (GET ONLY)
# ==============================================================
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().prefetch_related('productimage_set').select_related('category')
    serializer_class = ProductSerializer



# ==============================================================
#   CART VIEWSET
# ==============================================================
class CartViewSet(viewsets.ViewSet):

    # GET /api/cart/?user_id=1
    def list(self, request):
        user_id = request.GET.get("user_id")

        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)

        cart, created = Cart.objects.get_or_create(user_id=user_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # POST /api/cart/add_item/
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        cart, created = Cart.objects.get_or_create(user_id=user_id)
        product = Product.objects.get(product_id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()

        return Response({"message": "Item added to cart"})

    # POST /api/cart/remove_item/
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart_item_id = request.data.get('cart_item_id')

        try:
            CartItem.objects.get(cart_item_id=cart_item_id).delete()
            return Response({"message": "Item removed"})
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=400)



# ==============================================================
#   ORDER VIEWSET
# ==============================================================
class OrderViewSet(viewsets.ViewSet):

    # GET /api/orders/?user_id=1
    def list(self, request):
        user_id = request.GET.get("user_id")
        orders = Order.objects.filter(user_id=user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    # POST /api/orders/place/
    @action(detail=False, methods=['post'])
    def place(self, request):
        user_id = request.data.get('user_id')
        address_id = request.data.get('address_id')

        cart = Cart.objects.get(user_id=user_id)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            return Response({"error": "Cart is empty"}, status=400)

        total = 0
        for item in cart_items:
            total += float(item.product.discount_price) * item.quantity

        order = Order.objects.create(
            user_id=user_id,
            address_id=address_id,
            total_amount=total,
            status="Processing"
        )

        # Move cart items to order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.discount_price
            )

        cart_items.delete()  # clear cart

        return Response({"message": "Order placed", "order_id": order.order_id})
