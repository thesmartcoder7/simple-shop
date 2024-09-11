from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

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
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'session_key', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.price for item in obj.items.all())

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    selected_options = PartOptionSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'selected_options', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'session_key', 'items', 'status', 'total_price', 'created_at', 'updated_at']