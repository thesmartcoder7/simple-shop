from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Represents product categories (e.g., Bicycles, Skis, etc.)
    """
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# This model represents product categories (e.g., Bicycles, Skis, etc.)

class Product(models.Model):
    """
    Represents individual products (e.g., a specific bicycle model)
    """
    name = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} ({self.category})"

# Product model represents individual products (e.g., a specific bicycle model)
# It's linked to a Category and has a base price

class PartType(models.Model):
    """
    Represents different customizable parts of a product (e.g., Frame, Wheels)
    """
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} for {self.product}"

    class Meta:
        verbose_name = "Part Type"
        verbose_name_plural = "Part Types"

# PartType represents different customizable parts of a product (e.g., Frame, Wheels)
# It's associated with a specific Product

class PartOption(models.Model):
    """
    Represents specific options for each PartType (e.g., Full-suspension frame)
    """
    name = models.CharField(max_length=100)
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.part_type})"

    class Meta:
        verbose_name = "Part Option"
        verbose_name_plural = "Part Options"

# PartOption represents specific options for each PartType (e.g., Full-suspension frame)
# It includes a price and stock status

class Incompatibility(models.Model):
    """
    Stores pairs of PartOptions that can't be selected together
    """
    part_option_1 = models.ForeignKey(PartOption, on_delete=models.CASCADE, related_name='incompatibilities_1')
    part_option_2 = models.ForeignKey(PartOption, on_delete=models.CASCADE, related_name='incompatibilities_2')

    def __str__(self):
        return f"Incompatibility: {self.part_option_1} and {self.part_option_2}"

    class Meta:
        verbose_name_plural = "Incompatibilities"

# Incompatibility model stores pairs of PartOptions that can't be selected together

class PriceRule(models.Model):
    """
    Allows for complex pricing based on combinations of PartOptions
    """
    part_options = models.ManyToManyField(PartOption)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Price Rule: {self.price_adjustment:.2f}"

    class Meta:
        verbose_name = "Price Rule"
        verbose_name_plural = "Price Rules"

# PriceRule allows for complex pricing based on combinations of PartOptions

class Order(models.Model):
    """
    Contains general order information
    """
    PENDING = 'P'
    PROCESSING = 'PR'
    SHIPPED = 'S'
    DELIVERED = 'D'
    CANCELLED = 'C'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} ({self.get_status_display()})"

class OrderItem(models.Model):
    """
    Represents a single item in an order, including selected options and final price
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(PartOption)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product} in Order {self.order.id}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

# Add a Cart model for holding items before creating an order
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(PartOption)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product} in {self.cart}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"