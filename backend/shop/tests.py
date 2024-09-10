import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Category, Product, PartType, PartOption, Incompatibility, PriceRule, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, PartTypeSerializer, CartSerializer, OrderSerializer

@pytest.mark.django_db
class TestModels:
    """
    Test class for all model-related tests.
    This class contains tests for string representations and basic model functionality
    for Category, Product, PartType, PartOption, Incompatibility, PriceRule, Order, OrderItem, Cart, and CartItem models.
    """

    def test_category_str(self):
        category = Category.objects.create(name="Bicycles")
        assert str(category) == "Bicycles"

    def test_product_str(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)
        assert str(product) == "Mountain Bike (Bicycles)"

    def test_part_type_str(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)
        part_type = PartType.objects.create(name="Frame", product=product)
        assert str(part_type) == "Frame for Mountain Bike (Bicycles)"

    def test_part_option_str(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)
        part_type = PartType.objects.create(name="Frame", product=product)
        part_option = PartOption.objects.create(name="Aluminum", part_type=part_type, price=100.00)
        assert str(part_option) == "Aluminum (Frame for Mountain Bike (Bicycles))"

    def test_incompatibility(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)
        part_type = PartType.objects.create(name="Frame", product=product)
        option1 = PartOption.objects.create(name="Aluminum", part_type=part_type, price=100.00)
        option2 = PartOption.objects.create(name="Carbon", part_type=part_type, price=200.00)
        incompatibility = Incompatibility.objects.create(part_option_1=option1, part_option_2=option2)
        assert str(incompatibility) == f"Incompatibility: {option1} and {option2}"

    def test_price_rule(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)
        part_type = PartType.objects.create(name="Frame", product=product)
        option = PartOption.objects.create(name="Aluminum", part_type=part_type, price=100.00)
        price_rule = PriceRule.objects.create(price_adjustment=50.00)
        price_rule.part_options.add(option)
        assert str(price_rule) == "Price Rule: 50.00"

    def test_order(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        order = Order.objects.create(user=user, total_price=600.00)
        assert str(order) == f"Order {order.id} by testuser (Pending)"

    def test_order_item(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)
        order = Order.objects.create(user=user, total_price=600.00)
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1, price=600.00)
        assert str(order_item) == f"1x Mountain Bike (Bicycles) in Order {order.id}"

    def test_cart(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        cart = Cart.objects.create(user=user)
        assert str(cart) == "Cart for testuser"

    def test_cart_item(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)
        cart = Cart.objects.create(user=user)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1, price=500.00)
        assert str(cart_item) == f"1x Mountain Bike (Bicycles) in Cart for testuser"

@pytest.mark.django_db
class TestViews:
    """
    Test class for all view-related tests.
    This class contains tests for API endpoints including product detail, price calculation,
    adding to cart, viewing cart, creating orders, and listing orders.
    It tests the functionality and responses of these API views.
    """

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="testpass")

    @pytest.fixture
    def product(self):
        category = Category.objects.create(name="Bicycles")
        return Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)

    def test_product_detail_view(self, api_client, product):
        url = reverse('product-detail', kwargs={'product_id': product.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['product']['name'] == "Mountain Bike"

    def test_calculate_price_view(self, api_client, product):
        part_type = PartType.objects.create(name="Frame", product=product)
        option = PartOption.objects.create(name="Aluminum", part_type=part_type, price=100.00)
        url = reverse('calculate-price')
        data = {
            'product_id': product.id,
            'selected_options': [option.id]
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert response.data['price'] == 600.00

    def test_add_to_cart_view(self, api_client, user, product):
        api_client.force_authenticate(user=user)
        part_type = PartType.objects.create(name="Frame", product=product)
        option = PartOption.objects.create(name="Aluminum", part_type=part_type, price=100.00)
        url = reverse('add-to-cart')
        data = {
            'product_id': product.id,
            'selected_options': [option.id],
            'quantity': 1
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Cart.objects.filter(user=user).exists()
        assert CartItem.objects.filter(cart__user=user).count() == 1

    def test_cart_view(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('cart')
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_order_view(self, api_client, user, product):
        api_client.force_authenticate(user=user)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1, price=500.00)
        url = reverse('create-order')
        response = api_client.post(url)
        assert response.status_code == 201
        assert Order.objects.filter(user=user).exists()

    def test_order_list_view(self, api_client, user):
        api_client.force_authenticate(user=user)
        Order.objects.create(user=user, total_price=500.00)
        url = reverse('order-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1

@pytest.mark.django_db
class TestSerializers:
    """
    Test class for all serializer-related tests.
    This class contains tests for the serializers including ProductSerializer, PartTypeSerializer,
    CartSerializer, and OrderSerializer. It verifies that these serializers correctly represent
    the data of their respective models.
    """

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="testpass")

    @pytest.fixture
    def product(self):
        category = Category.objects.create(name="Bicycles")
        return Product.objects.create(name="Mountain Bike", category=category, base_price=500.00)

    def test_product_serializer(self, product):
        serializer = ProductSerializer(product)
        assert serializer.data['name'] == "Mountain Bike"
        assert serializer.data['base_price'] == "500.00"

    def test_part_type_serializer(self, product):
        part_type = PartType.objects.create(name="Frame", product=product)
        PartOption.objects.create(name="Aluminum", part_type=part_type, price=100.00)
        serializer = PartTypeSerializer(part_type)
        assert serializer.data['name'] == "Frame"
        assert len(serializer.data['options']) == 1

    def test_cart_serializer(self, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1, price=500.00)
        serializer = CartSerializer(cart)
        assert len(serializer.data['items']) == 1

    def test_order_serializer(self, user, product):
        order = Order.objects.create(user=user, total_price=500.00)
        OrderItem.objects.create(order=order, product=product, quantity=1, price=500.00)
        serializer = OrderSerializer(order)
        assert serializer.data['total_price'] == "500.00"
        assert len(serializer.data['items']) == 1