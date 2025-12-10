from django.db import models


# ===========================
#  USERS TABLE
# ===========================
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'users'
        managed = False   # IMPORTANT

    def __str__(self):
        return self.name


# ===========================
#  ADDRESSES TABLE
# ===========================
class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)

    class Meta:
        db_table = 'ADDRESSES'
        managed = False   # IMPORTANT

    def __str__(self):
        return f"{self.full_name} - {self.city}"


# ===========================
#  CATEGORIES TABLE
# ===========================
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'CATEGORIES'
        managed = False   # IMPORTANT

    def __str__(self):
        return self.name


# ===========================
#  PRODUCTS TABLE
# ===========================
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        db_table = 'PRODUCTS'
        managed = False   # IMPORTANT

    def __str__(self):
        return self.name


# ===========================
#  PRODUCT IMAGES TABLE
# ===========================
class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)

    class Meta:
        db_table = 'PRODUCT_IMAGES'
        managed = False   # IMPORTANT

    def __str__(self):
        return self.image_url


# ===========================
#  CART TABLE
# ===========================
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CART'
        managed = False   # IMPORTANT

    def __str__(self):
        return f"Cart {self.cart_id}"


# ===========================
#  CART ITEMS TABLE
# ===========================
class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'CART_ITEMS'
        managed = False   # IMPORTANT

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# ===========================
#  ORDERS TABLE
# ===========================
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'ORDERS'
        managed = False   # IMPORTANT

    def __str__(self):
        return f"Order {self.order_id}"


# ===========================
#  ORDER ITEMS TABLE
# ===========================
class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ORDER_ITEMS'
        managed = False   # IMPORTANT

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
