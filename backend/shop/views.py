from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, PartType, PartOption, PriceRule, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, PartTypeSerializer, CartSerializer, OrderSerializer
from decimal import Decimal

class ProductDetailView(APIView):
    """
    API view to retrieve details of a specific product
    """
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

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data['product_id']
        selected_option_ids = request.data['selected_options']
        quantity = int(request.data.get('quantity', 1))  # Ensure quantity is an integer

        try:
            product = Product.objects.get(id=product_id)
            selected_options = PartOption.objects.filter(id__in=selected_option_ids)

            # Calculate price
            total_price = Decimal(product.base_price)  # Convert to Decimal
            for option in selected_options:
                total_price += Decimal(option.price)  # Convert to Decimal

            # Apply price rules
            price_rules = PriceRule.objects.filter(part_options__in=selected_options).distinct()
            for rule in price_rules:
                if set(rule.part_options.all()).issubset(set(selected_options)):
                    total_price += Decimal(rule.price_adjustment)  # Convert to Decimal

            # Get or create cart
            cart, _ = Cart.objects.get_or_create(user=request.user)

            # Create cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                price=total_price * quantity
            )
            cart_item.selected_options.set(selected_options)

            return Response({'success': True}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.price for item in cart.items.all())
        
        order = Order.objects.create(
            user=request.user,
            total_price=total_price
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
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)