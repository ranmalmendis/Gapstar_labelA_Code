from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Ensures that only authenticated users can access these views
from .models import ShoppingCart, CartItem, Order
from .serializers import CartItemSerializer, OrderSerializer,AddToCartSerializer,RemoveFromCartSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.http import JsonResponse
from .models import Product  
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class AddToCartView(APIView):
    """
    Allows authenticated users to add products to their shopping cart.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
    
    @swagger_auto_schema(request_body=AddToCartSerializer)
    def post(self, request, *args, **kwargs):
        
        """
        Handles POST request to add a product by ID to the user's shopping cart,
        creating the cart if it doesn't exist, and updating the quantity of the product if it's already in the cart.
        """
        product_id=""
        # Inside your AddToCartView.post method
        product_id = request.data.get('product_id')
        if not product_id:
            return JsonResponse({'error': 'product_id is required'}, status=400)
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'error': 'Invalid product_id'}, status=404)

       
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # Default quantity is 1 if not specified
        # Retrieve or create the shopping cart for the current user
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        # Retrieve or create the cart item for the specified product, updating the quantity if the item already exists
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product_id=product_id, 
            defaults={'quantity': quantity}
        )
        if not created:
            # If the item already exists, just update its quantity
            cart_item.quantity += int(quantity)
            cart_item.save()
        # Serialize the cart item to return its details in the response
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

class RemoveFromCartView(APIView):
    """
    Allows authenticated users to remove products from their shopping cart.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RemoveFromCartSerializer)

    def post(self, request, *args, **kwargs):
        product_id=""
        # Inside your AddToCartView.post method
        product_id = request.data.get('product_id')
        if not product_id:
                return JsonResponse({'error': 'product_id is required'}, status=400)
  
        """
        Handles POST request to remove a product by ID from the user's shopping cart,
        adjusting the quantity or removing the item entirely if necessary.
        """
        product_id = request.data.get('product_id')
        # Retrieve the user's shopping cart and the specified cart item
        cart = get_object_or_404(ShoppingCart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        if cart_item.quantity >= 1:
            # If more than one, decrease the quantity
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # If only one, remove the item from the cart
            cart_item.delete()
        return Response({'status': 'Item removed'})

class CreateOrderView(APIView):
    """
    Allows authenticated users to create an order from their shopping cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to convert the user's shopping cart into an order,
        requiring the user to specify a delivery date and time.
        """
        # Ensure the user has a shopping cart without an associated order
        cart = get_object_or_404(ShoppingCart, user=request.user, order=None)
        delivery_date = request.data.get('delivery_date')
        delivery_time = request.data.get('delivery_time')
        if delivery_date and delivery_time:
            # Create the order with the specified delivery date and time
            order = Order.objects.create(
                cart=cart,
                user=request.user,
                delivery_date=delivery_date,
                delivery_time=delivery_time
            )
            # Serialize the order to return its details in the response
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            # If delivery date or time is not specified, return an error
            return Response({'error': 'Delivery date and time are required'}, status=400)

class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # This viewset automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
