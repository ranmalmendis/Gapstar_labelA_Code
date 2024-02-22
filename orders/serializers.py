import logging
from rest_framework import serializers
from .models import CartItem, Order
from django.contrib.auth import get_user_model
from django.db import IntegrityError

logger = logging.getLogger(__name__)

# This allows the serializer to reference the correct user model.
User = get_user_model()

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.

    This serializer is responsible for converting CartItem model instances into a JSON format and
    vice versa, specifying which fields should be included in the serialized output.
    """
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    In addition to serializing model fields, this serializer includes a read-only field to
    represent the total_order_price. This calculated property comes from the associated
    ShoppingCart's items, encapsulating the logic within the model for data representation.
    """
    total_order_price = serializers.ReadOnlyField()
    delivery_time = serializers.TimeField(format='%H:%M:%S', default='12:00:00', help_text="Default delivery time is 12:00:00")


    class Meta:
        model = Order
        fields = ['id', 'cart', 'user', 'ordered_at', 'delivery_date', 'delivery_time', 'total_order_price']
        read_only_fields = ['id','cart','user','ordered_at', 'total_order_price']


    def create(self, validated_data):
        try:
            order = super().create(validated_data)
            order.cart.status = 'completed'  # Mark the cart as completed
            order.cart.save()
            return order
        except IntegrityError as e:
            logger.error(f"Error creating order due to cart uniqueness constraint: {e}")
            raise serializers.ValidationError({"cart": "This cart has already been used for an order."})
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise serializers.ValidationError("An error occurred during order creation.")


    
    def update(self, instance, validated_data):
        """
        Overridden update method to implement custom logic upon updating an Order instance.
        """
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            logger.error(f"Error updating order: {e}")
            raise serializers.ValidationError("An error occurred during order update.")


class AddToCartSerializer(serializers.Serializer):
    """
    Serializer for adding items to the shopping cart.

    Validates the product ID and quantity before adding them to the cart.
    """
    product_id = serializers.IntegerField(help_text='ID of the product to add')
    quantity = serializers.IntegerField(default=1, help_text='Quantity of the product')


class RemoveFromCartSerializer(serializers.Serializer):
    """
    Serializer for removing items from the shopping cart.

    Validates the product ID and quantity before removing them from the cart.
    """
    product_id = serializers.IntegerField(help_text='ID of the product to remove')
    quantity = serializers.IntegerField(default=1, help_text='Quantity of the product to remove')