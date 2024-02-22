from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from .models import ShoppingCart, CartItem, Order
from .serializers import CartItemSerializer, OrderSerializer,AddToCartSerializer,RemoveFromCartSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from django.http import JsonResponse
from .models import Product  
from drf_yasg.utils import swagger_auto_schema
import logging
from django.db import transaction


logger = logging.getLogger(__name__)


class AddToCartView(APIView):
    """
    View for adding products to the shopping cart of an authenticated user. It checks for the existence of the product
    and the shopping cart, creates or updates the cart item with the specified quantity, and returns the updated cart item.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AddToCartSerializer)
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data.get('quantity', 1)  # Default quantity to 1 if not specified

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                logger.error(f"Product with id {product_id} does not exist.")
                return Response({'error': 'Invalid Product ID'}, status=status.HTTP_404_NOT_FOUND)

            # Check if there's an active cart; if not, create a new one.
            cart, created = ShoppingCart.objects.get_or_create(
                user=request.user, 
                status='active', 
                defaults={
                    'user': request.user,
                    'status': 'active'
                }
            )

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                # If the item already exists in the cart, update the quantity
                cart_item.quantity += int(quantity)
                cart_item.save()

            # Serialize the cart item to return
            cart_item_serializer = CartItemSerializer(cart_item)
            return Response(cart_item_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RemoveFromCartView(APIView):
    """
    API view that allows authenticated users to remove products from their shopping cart.
    Users can adjust the quantity of an existing cart item or remove it entirely if the quantity is one.
    """
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=RemoveFromCartSerializer)
    def post(self, request, *args, **kwargs):
        """
        Receives a POST request with a product ID and removes the specified product from the user's shopping cart.
        Adjusts the quantity of the cart item or removes it entirely if necessary.
        """
        product_id = request.data.get('product_id')
        if not product_id:
            logger.error("Product ID not provided in the request.")
            return JsonResponse({'error': 'product_id is required'}, status=400)
        
        try:
            cart = get_object_or_404(ShoppingCart, user=request.user)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                logger.info(f"Decreased quantity of product ID {product_id} for user {request.user.username}.")
            else:
                cart_item.delete()
                logger.info(f"Removed product ID {product_id} from user {request.user.username}'s cart.")
                
            return Response({'status': 'Item removed'})
        except Exception as e:
            logger.error(f"Error removing product from cart: {str(e)}")
            return JsonResponse({'error': 'An error occurred while removing the item from the cart'}, status=500)



class CreateOrderView(APIView):
    """
    View to allow authenticated users to create an order from their shopping cart.
    
    This view assumes the existence of an 'active' status for shopping carts,
    indicating carts that are currently in use and not yet converted into orders.
    Once an order is created, the cart's status is updated to 'completed' to prevent further modifications.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        
        if serializer.is_valid():
            with transaction.atomic():
                cart = ShoppingCart.objects.filter(user=request.user, status='active').order_by('-created_at').first()
                print("Cart is ", cart)
                if not cart:
                    logger.error(f"No active shopping cart found for user: {request.user}")
                    return Response({'error': 'No active shopping cart found.'}, status=status.HTTP_404_NOT_FOUND)

                # Assuming 'delivery_date' and 'delivery_time' are validated by the serializer
                delivery_date = serializer.validated_data.get('delivery_date')
                delivery_time = serializer.validated_data.get('delivery_time')

                order = Order.objects.create(
                    cart=cart,
                    user=request.user,
                    delivery_date=delivery_date,
                    delivery_time=delivery_time
                )

                # Mark the cart as completed
                cart.status = 'completed'
                cart.save()

                # Instead of serializing the order again, use the validated data and add the order id
                response_data = serializer.validated_data
                response_data['id'] = order.id

                return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

          
class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing orders.

    Provides `list`, `create`, `retrieve`, `update`, and `destroy` actions automatically.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        """
        List all orders.
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error listing orders: {e}")
            return Response({"error": "Error listing orders"}, status=400)

    def create(self, request, *args, **kwargs):
        """
        Create a new order.
        """
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return Response({"error": "Error creating order"}, status=400)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific order.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving order: {e}")
            return Response({"error": "Error retrieving order"}, status=400)

    def update(self, request, *args, **kwargs):
        """
        Update an order.
        """
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error updating order: {e}")
            return Response({"error": "Error updating order"}, status=400)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an order.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting order: {e}")
            return Response({"error": "Error deleting order"}, status=400)