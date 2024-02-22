from django.db import models
import logging

logger = logging.getLogger(__name__)

class Product(models.Model):
    """
    Represents a product with attributes for name, description, price, and stock quantity.
    The model includes fields for storing product details and methods for product representation.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        """
        Returns a string representation of the product, primarily the product name.
        Useful for admin panels, debugging, and any human-readable representation needs.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Overridden save method to include error logging for database operations.
        Ensures that any database errors are logged when attempting to save a product.
        """
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving Product {self.name}: {e}")
            raise
