"""Customer order module."""

from django.db import models
from shops.models import Product


class Order(models.Model):
    """Register a new Order in the database."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        """Order meta information."""

        ordering = ('-created',)

    def __str__(self):
        """String representation of order."""
        return f'Order {self.id}'

    def get_total_cost(self):
        """Retrieve total cost."""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Order item."""

    order = models.ForeignKey(
        Order, related_name='items',
        on_delete=models.CASCADE
        )
    product = models.ForeignKey(
        Product, related_name='order_items',
        on_delete=models.CASCADE
        )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        """String representation of the model."""
        return str(self.id)

    def get_cost(self):
        """Retrieve the cost of the product."""
        return self.price * self.quantity