import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from products.models import Product
from .serializers import ProductSerializer

# Configure logging
logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    """
    Provides a full set of CRUD operations for Product entities using Django REST Framework's ModelViewSet.
    
    Attributes:
        queryset: Specifies the list of items for this viewset.
        serializer_class: Defines the serializer class for serializing and deserializing the Product instances.
    
    Automatically provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    Utilizes DRF's built-in pagination for efficient data retrieval.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        """
        Overrides the list method to provide custom error handling and logging.
        Returns a paginated list of Product instances or an error message upon failure.
        """
        try:
            # Pagination is handled by DRF's settings; no need for manual pagination here.
            # Just call the super method and let DRF handle the rest.
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error fetching product list: {e}")
            return Response({"error": f"Did you enter the correct page number; {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
