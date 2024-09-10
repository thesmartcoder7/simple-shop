from rest_framework import serializers
from .models import Product, PartType, PartOption, Cart, CartItem, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'base_price']

class PartOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartOption
        fields = ['id', 'name', 'price', 'in_stock']

class PartTypeSerializer(serializers.ModelSerializer):
    options = PartOptionSerializer(source='partoption_set', many=True, read_only=True)

    class Meta:
        model = PartType
        fields = ['id', 'name', 'options']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    selected_options = PartOptionSerializer(many=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'selected_options', 'quantity', 'price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    selected_options = PartOptionSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'selected_options', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'status', 'total_price', 'created_at', 'updated_at']