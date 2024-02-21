from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Define the serializer for the Product model. Meta class is used to specify which model the serializer should be based on
    and which fields should be included in the serialized output. """
    class Meta:
        model = Product  # Specifies that the serializer is for the Product model.
        # Defines the fields that should be included in the serialization. 
        # This allows for both serialization (converting querysets and model instances to Python datatypes) 
        # and deserialization (validating and converting incoming data back to complex types, after validating the incoming data).
        fields = ['id', 'name', 'description', 'price', 'stock_quantity']  
        # id: The primary key of the Product.
        # name: The name of the Product.
        # description: A detailed description of the Product.
        # price: The price of the Product. This field uses DecimalField to accurately handle decimal numbers.
        # stock_quantity: The quantity of the Product available in stock.
        
    