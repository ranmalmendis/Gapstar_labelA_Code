from django.db import models

class Product(models.Model):
    # The `name` field stores the name of the product. It's a character field with a maximum length of 255 characters.
    # This limit ensures that product names are reasonably sized for display in UIs and for storage efficiency.
    name = models.CharField(max_length=255)

    # The `description` field holds a detailed description of the product. It uses Django's `TextField`,
    description = models.TextField()

    # The `price` field represents the price of the product. It's stored as a decimal field to accurately
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # The `stock_quantity` field represents how many units of the product are available in stock.
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        # The `__str__` method returns the product name when an instance of the `Product` model is
        # converted to a string. This is useful for admin panels, debugging, and any situation where
        # a human-readable representation of the product is needed.
        return self.name
