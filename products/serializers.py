import logging
from rest_framework import serializers
from .models import Product

# Configure logging
logger = logging.getLogger(__name__)

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    
    Serializes fields: id, name, description, price, and stock_quantity to Python data types for easy rendering to JSON or other content types. Also handles deserialization back to complex types after validating the incoming data.
    """
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity']

    # Example of a method with error handling (theoretical)
    def validate_price(self, value):
        """
        Validates that the price of the product is not negative.
        
        Args:
            value (Decimal): The price value to validate.
            
        Returns:
            Decimal: The validated price.
            
        Raises:
            serializers.ValidationError: If the price is negative.
        """
        if value < 0:
            logger.error(f"Validation error: Negative price value {value} submitted.")
            raise serializers.ValidationError("Price must be a positive number.")
        return value
