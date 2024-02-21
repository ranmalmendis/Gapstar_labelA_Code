from django.db import models
from django.conf import settings
from products.models import Product

# Represents a user's shopping cart. Each user has a unique cart.
class ShoppingCart(models.Model):
    # Link to the user model, defined in settings.AUTH_USER_MODEL. 
    # Ensures one-to-one relationship, meaning each user can have only one shopping cart.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_cart')
    
    # Automatically sets the date and time when the shopping cart is created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation of the ShoppingCart model for admin and debugging purposes.
        return f"ShoppingCart({self.user.username})"

    # Calculates the total price of all items in the cart.
    # This is a dynamically computed property, not stored in the database.
    @property
    def total_price(self):
        # Sums up the total price for each CartItem associated with this ShoppingCart.
        return sum(item.total_price for item in self.items.all())

# Represents an individual item within a shopping cart.
class CartItem(models.Model):
    # Links the CartItem to the ShoppingCart. A ShoppingCart can have multiple CartItems.
    cart = models.ForeignKey(ShoppingCart, related_name='items', on_delete=models.CASCADE)
    
    # Links the CartItem to a specific Product. This establishes what product the item represents.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Stores the quantity of the product. PositiveIntegerField ensures that the quantity is always a positive number.
    quantity = models.PositiveIntegerField(default=1)
    
    # Automatically sets the date and time when the item is added to the cart.
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation includes the product name and quantity for clarity.
        return f"CartItem(Product: {self.product.name}, Quantity: {self.quantity})"

    # Calculates the total price for this item (quantity * product price).
    # This is a dynamically computed property, not stored in the database.
    @property
    def total_price(self):
        # Multiplies the product's price by the item's quantity to get the total price for this item.
        return self.quantity * self.product.price

# Represents an order created from a shopping cart.
class Order(models.Model):
    # Links the Order to the ShoppingCart it was created from.
    # Ensures a one-to-one relationship, meaning each shopping cart can only be associated with one order.
    cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE, related_name='order')
    
    # Links the Order to the user who made it.
    # A user can have multiple orders, so this is a ForeignKey relationship.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    
    # Automatically sets the date and time when the order is placed.
    ordered_at = models.DateTimeField(auto_now_add=True)
    
    # The date the order is scheduled for delivery.
    delivery_date = models.DateField()
    
    # The time the order is scheduled for delivery.
    delivery_time = models.TimeField()

    def __str__(self):
        # String representation includes the username and the date the order was placed.
        return f"Order({self.user.username}, {self.ordered_at.date()})"

    # Leverages the ShoppingCart's total_price property to calculate the total price of the order.
    # This is a dynamically computed property, not stored in the database.
    @property
    def total_order_price(self):
        # Returns the total price of all items in the linked ShoppingCart.
        return self.cart.total_price
