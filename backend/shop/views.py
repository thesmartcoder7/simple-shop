from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from decimal import Decimal
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

class BaseView(APIView):
    def get_session_key(self, request):
        session_key = request.META.get('HTTP_X_SESSION_KEY')
        if session_key:
            session = SessionStore(session_key=session_key)
            if session.exists(session_key):
                return session_key
        return request.session.session_key or request.session.create()

class ProductListView(ListAPIView):
    """
    API view to retrieve a list of all products
    """
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(APIView):
    """
    API view to retrieve details of a specific product
    """
    permission_classes = [AllowAny]
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            part_types = PartType.objects.filter(product=product)
            
            data = {
                'product': ProductSerializer(product).data,
                'part_types': PartTypeSerializer(part_types, many=True).data
            }
            return Response(data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class CalculatePriceView(APIView):
    """
    API view to calculate the price of a product based on selected options
    """
    def post(self, request):
        product_id = request.data['product_id']
        selected_option_ids = request.data['selected_options']
        
        try:
            product = Product.objects.get(id=product_id)
            selected_options = PartOption.objects.filter(id__in=selected_option_ids)
            
            # Start with base price
            total_price = product.base_price
            
            # Add individual option prices
            for option in selected_options:
                total_price += option.price
            
            # Apply price rules
            price_rules = PriceRule.objects.filter(part_options__in=selected_options).distinct()
            for rule in price_rules:
                # Check if all part options in the rule are selected
                if set(rule.part_options.all()).issubset(set(selected_options)):
                    total_price += rule.price_adjustment
            
            return Response({'price': total_price})
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class AddToCartView(BaseView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_key = self.get_session_key(request)
        product_id = request.data['product_id']
        selected_option_ids = request.data['selected_options']
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
            selected_options = PartOption.objects.filter(id__in=selected_option_ids)

            # Calculate price
            total_price = Decimal(product.base_price)
            for option in selected_options:
                total_price += Decimal(option.price)

            # Apply price rules
            price_rules = PriceRule.objects.filter(part_options__in=selected_options).distinct()
            for rule in price_rules:
                if set(rule.part_options.all()).issubset(set(selected_options)):
                    total_price += Decimal(rule.price_adjustment)

            # Get or create cart
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            cart, _ = Cart.objects.get_or_create(session_key=session_key)

            # Create cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                price=total_price * quantity
            )
            cart_item.selected_options.set(selected_options)

            return Response({
            'success': True,
            'session_key': session_key
        }, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class CartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        session_key = request.META.get('HTTP_X_SESSION_KEY') or request.session.session_key
        if not session_key:
            session_key = request.session.create()

        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CreateOrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_key = request.META.get('HTTP_X_SESSION_KEY') or request.session.session_key
        if not session_key:
            return Response({'error': 'No active session'}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(session_key=session_key).first()
        if not cart or not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.price for item in cart.items.all())
        
        order = Order.objects.create(
            session_key=session_key,
            total_price=total_price,
            status=Order.PENDING
        )

        for cart_item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price
            )
            order_item.selected_options.set(cart_item.selected_options.all())

        # Clear the cart
        cart.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
