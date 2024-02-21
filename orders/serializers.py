from rest_framework import serializers
from .models import CartItem, Order
from django.contrib.auth import get_user_model

# Get the User model from Django's authentication system.
# This allows the serializer to reference the correct user model, 
# regardless of whether the default user model or a custom user model is being used.
User = get_user_model()

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model.

    This serializer translates the CartItem model instances into a format that can be easily rendered into JSON.
    It specifies which fields should be included in the serialized output.
    """
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']
        # Specifies the model to be serialized and the fields to be included.

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.

    In addition to serializing model fields, this serializer includes a read-only field
    to represent the total_order_price, which is a property calculated from the associated ShoppingCart's items.
    This approach encapsulates the logic for calculating the total order price within the model,
    ensuring that the serializer remains focused on data representation.
    """
    # A read-only field that dynamically retrieves the total_order_price from the Order model's property.
    # This field is not directly associated with a model field but is derived from the order's cart.
    total_order_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'cart', 'user', 'ordered_at', 'delivery_date', 'delivery_time', 'total_order_price']
        read_only_fields = ['id', 'ordered_at', 'total_order_price']
        # id, ordered_at, and total_order_price fields are marked as read-only to prevent them from being
        # altered through the API, thereby preserving the integrity of the data.

    def create(self, validated_data):
        """
        Custom creation logic for an Order instance.

        This method can be overridden to include business logic that needs to be executed
        when a new Order instance is created. For instance, setting additional fields
        or modifying the validated_data before creating the Order instance.
        """
        # Calls the superclass's create method with the validated data.
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Custom update logic for an Order instance.

        This method can be overridden to implement custom update logic.
        For example, it could be used to enforce certain constraints or to trigger
        additional actions after an Order instance is updated.
        """
        # Calls the superclass's update method with the instance and the validated data.
        return super().update(instance, validated_data)


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(help_text='ID of the product to add')
    quantity = serializers.IntegerField(default=1, help_text='Quantity of the product')


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(help_text='ID of the product to add')
    quantity = serializers.IntegerField(default=1, help_text='Quantity of the product')