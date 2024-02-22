import logging
from django.db import models
from django.conf import settings
from products.models import Product

import logging

logger = logging.getLogger(__name__)


class ShoppingCart(models.Model):
    """
    A shopping cart model that represents a unique cart for each user, ensuring a one-to-one relationship
    with the user model defined in settings.AUTH_USER_MODEL. It includes a creation timestamp and a method
    to calculate the total price of all items in the cart.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='shopping_carts',  # Change to plural as a user can have multiple carts
        verbose_name="User",
        help_text="The user this shopping cart belongs to."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Created At",
        help_text="Timestamp when the shopping cart was created."
    )
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('completed', 'Completed')],
        default='active',
        help_text="The status of the shopping cart."
    )

    def __str__(self):
        return f"ShoppingCart({self.user.username}, Status: {self.status})"

    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            try:
                total += item.total_price
            except Exception as e:
                logger.error(f"Error calculating total price for item {item.id} in ShoppingCart {self.id}: {e}")
                continue
        return total

    @property
    def total_price(self):
        """
        Calculates the total price of all items in the shopping cart. If any item's price is undefined,
        it gracefully handles the error and continues with other items.

        Returns:
            Decimal: The total price of all valid items in the shopping cart.
        """
        total = 0
        for item in self.items.all():
            try:
                total += item.total_price
            except AttributeError:
                logger.error(f"Error calculating total price for item {item.id} in ShoppingCart {self.id}: ")

                continue
            
        return total


class CartItem(models.Model):
    """
    Represents an individual item within a shopping cart, linking a specific product
    with a quantity to a ShoppingCart instance.
    """

    cart = models.ForeignKey(
        'ShoppingCart', 
        related_name='items', 
        on_delete=models.CASCADE,
        help_text="The shopping cart to which this item belongs."
    )
    product = models.ForeignKey(
        'products.Product', 
        on_delete=models.CASCADE,
        help_text="The specific product this cart item represents."
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="The quantity of the product."
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The datetime when the item was added to the cart."
    )

    def __str__(self):
        """Returns a readable string representation of the CartItem instance."""
        return f"CartItem(Product: {self.product.name}, Quantity: {self.quantity})"

    @property
    def total_price(self):
        """
        Calculates and returns the total price for this cart item as the product
        of its quantity and the associated product's price. Includes error handling
        to log issues when calculating the total price.
        """
        try:
            return self.quantity * self.product.price
        except TypeError:
            logger.error(f"Error calculating total price for CartItem {self.id}: Invalid type.")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error calculating total price for CartItem {self.id}: {e}")
            return 0

class Order(models.Model):
    """
    Represents an order created from a shopping cart, linking it to the ShoppingCart
    it originated from and the user who made the order. It includes details about 
    the order timing and delivery schedule.
    
    Attributes:
        cart (OneToOneField): A one-to-one link to the ShoppingCart.
        user (ForeignKey): A link to the user who placed the order, supporting multiple orders per user.
        ordered_at (DateTimeField): The timestamp when the order was placed.
        delivery_date (DateField): The scheduled delivery date for the order.
        delivery_time (TimeField): The scheduled delivery time for the order.
    """
    
    cart = models.OneToOneField(
        'ShoppingCart',
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name="Linked shopping cart"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Ordering user"
    )
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="Order timestamp")
    delivery_date = models.DateField(verbose_name="Scheduled delivery date")
    delivery_time = models.TimeField(verbose_name="Scheduled delivery time")

    def __str__(self):
        """Provides a human-readable string representation of the order."""
        return f"Order(user={self.user.username}, date={self.ordered_at.date()})"

    @property
    def total_order_price(self):
        """
        Calculates the total price of the order by leveraging the ShoppingCart's
        total_price property. This dynamically computed property is not stored in the database.
        
        Returns:
            Decimal: Total price of all items in the linked ShoppingCart.
        """
        try:
            return self.cart.total_price
        except Exception as e:
            logger.error(f"Error calculating total_order_price: {e}")
            return 0