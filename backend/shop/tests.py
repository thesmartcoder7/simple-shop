import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import *
from .serializers import *

@pytest.mark.django_db
class TestModels:
    def test_category_creation(self):
        category = Category.objects.create(name="Bicycles")
        assert category.name == "Bicycles"
        assert str(category) == "Bicycles"

    def test_product_creation(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        assert product.name == "Mountain Bike"
        assert product.category == category
        assert product.base_price == Decimal("500.00")
        assert str(product) == "Mountain Bike (Bicycles)"

    def test_part_type_creation(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        part_type = PartType.objects.create(name="Frame", product=product)
        assert part_type.name == "Frame"
        assert part_type.product == product
        assert str(part_type) == "Frame for Mountain Bike (Bicycles)"

    def test_incompatibility_creation(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        part_type = PartType.objects.create(name="Frame", product=product)
        option1 = PartOption.objects.create(name="Aluminum Frame", part_type=part_type, price=Decimal("100.00"))
        option2 = PartOption.objects.create(name="Carbon Frame", part_type=part_type, price=Decimal("200.00"))
        incompatibility = Incompatibility.objects.create(part_option_1=option1, part_option_2=option2)
        assert str(incompatibility) == f"Incompatibility: {option1} and {option2}"

    def test_price_rule_creation(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        part_type = PartType.objects.create(name="Frame", product=product)
        option = PartOption.objects.create(name="Aluminum Frame", part_type=part_type, price=Decimal("100.00"))
        price_rule = PriceRule.objects.create(price_adjustment=Decimal("-50.00"))
        price_rule.part_options.add(option)
        assert str(price_rule) == "Price Rule: -50.00"

    def test_order_creation(self):
        order = Order.objects.create(session_key="test_session", total_price=Decimal("600.00"))
        assert order.status == Order.PENDING
        assert str(order) == f"Order {order.id} by test_session (Pending)"

    def test_order_item_creation(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        order = Order.objects.create(session_key="test_session", total_price=Decimal("600.00"))
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1, price=Decimal("500.00"))
        assert str(order_item) == f"1x Mountain Bike (Bicycles) in Order {order.id}"

    def test_cart_creation(self):
        cart = Cart.objects.create(session_key="test_session")
        assert str(cart) == "Cart test_session"

    def test_cart_item_creation(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        cart = Cart.objects.create(session_key="test_session")
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1, price=Decimal("500.00"))
        assert str(cart_item) == f"1x Mountain Bike (Bicycles) in Cart test_session"

@pytest.mark.django_db
class TestSerializers:
    def test_category_serializer(self):
        category = Category.objects.create(name="Bicycles")
        serializer = CategorySerializer(category)
        assert serializer.data == {"id": category.id, "name": "Bicycles"}

    def test_product_serializer(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        serializer = ProductSerializer(product)
        assert serializer.data == {
            "id": product.id,
            "name": "Mountain Bike",
            "category": {"id": category.id, "name": "Bicycles"},
            "base_price": "500.00"
        }

    def test_part_option_serializer(self):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        part_type = PartType.objects.create(name="Frame", product=product)
        part_option = PartOption.objects.create(name="Aluminum Frame", part_type=part_type, price=Decimal("100.00"))
        serializer = PartOptionSerializer(part_option)
        assert serializer.data == {
            "id": part_option.id,
            "name": "Aluminum Frame",
            "price": "100.00",
            "in_stock": True
        }

    def test_cart_item_serializer(self):
        cart = Cart.objects.create(session_key="test_session")
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1, price=Decimal("500.00"))
        serializer = CartItemSerializer(cart_item)
        assert serializer.data["product"]["name"] == "Mountain Bike"
        assert serializer.data["quantity"] == 1
        assert serializer.data["price"] == "500.00"

    def test_order_serializer(self):
        order = Order.objects.create(session_key="test_session", total_price=Decimal("600.00"))
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        OrderItem.objects.create(order=order, product=product, quantity=1, price=Decimal("500.00"))
        serializer = OrderSerializer(order)
        assert serializer.data["session_key"] == "test_session"
        assert serializer.data["total_price"] == "600.00"
        assert len(serializer.data["items"]) == 1

    def test_order_item_serializer(self):
        order = Order.objects.create(session_key="test_session", total_price=Decimal("600.00"))
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1, price=Decimal("500.00"))
        serializer = OrderItemSerializer(order_item)
        assert serializer.data["product"]["name"] == "Mountain Bike"
        assert serializer.data["quantity"] == 1
        assert serializer.data["price"] == "500.00"

@pytest.mark.django_db
class TestViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_product_list_view(self, api_client):
        url = reverse('product-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_product_detail_view(self, api_client):
        category = Category.objects.create(name="Bicycles")
        product = Product.objects.create(name="Mountain Bike", category=category, base_price=Decimal("500.00"))
        url = reverse('product-detail', kwargs={'product_id': product.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['product']['name'] == "Mountain Bike"

    def test_product_list_view_empty(self, api_client):
        url = reverse('product-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_product_detail_view_not_found(self, api_client):
        url = reverse('product-detail', kwargs={'product_id': 999})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_add_to_cart_view_invalid_product(self, api_client):
        url = reverse('add-to-cart')
        data = {
            'product_id': 999,
            'selected_options': [],
            'quantity': 1
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_calculate_price_view_invalid_product(self, api_client):
        url = reverse('calculate-price')
        data = {
            'product_id': 999,
            'selected_options': []
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_order_view_empty_cart(self, api_client):
        url = reverse('create-order')
        api_client.cookies['sessionid'] = 'test_session'
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
