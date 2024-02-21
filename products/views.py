# Import necessary Django and Django REST Framework modules
from django.shortcuts import render  # Used for rendering HTML templates (not used in this API view but available if needed)
from rest_framework import viewsets  # Import the viewsets module from Django REST Framework

# Import the Product model and ProductSerializer from the current application's modules
from products.models import Product
from .serializers import ProductSerializer  # Import the ProductSerializer from the serializers.py file in the same directory

# Define a class-based view to handle CRUD operations for Product entities
class ProductViewSet(viewsets.ModelViewSet):
    """
    ProductViewSet extends ModelViewSet from Django REST Framework to provide 
    a full set of CRUD operations for Product entities.

    Attributes:
        queryset (queryset): The base queryset that the view will use to retrieve Product instances. 
                             This is set to retrieve all instances of the Product model.
        serializer_class (ProductSerializer): The serializer class that will be used to serialize and 
                                              deserialize Product instances. This controls how the 
                                              Product data is converted to and from JSON format when 
                                              handling HTTP requests.

    I ensure that this viewset is designed to be easily 
    extensible and maintainable, adhering to best practices in Django and Django REST Framework 
    development. It leverages Django's powerful ORM and REST Framework's serializers to provide 
    a robust API endpoint for managing Product data.
    """

    # Set the queryset to retrieve all Product instances from the database
    # This allows the viewset to know which records to include when responding to GET requests
    queryset = Product.objects.all()

    # Specify the serializer class to be used for serializing and deserializing data
    # The ProductSerializer is responsible for converting Product instances to JSON format and vice versa
    serializer_class = ProductSerializer
