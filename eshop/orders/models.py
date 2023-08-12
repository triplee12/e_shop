"""Customer order module."""

from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from shops.models import Product
from coupons.models import Coupon


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
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(
        Coupon, related_name='orders',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0), MaxValueValidator(100)
        ]
    )

    class Meta:
        """Order meta information."""

        ordering = ('-created',)

    def __str__(self):
        """String representation of order."""
        return f'Order {self.id}'

    def get_total_cost(self):
        """Retrieve total cost."""
        total_cost = sum(
            item.get_cost() for item in self.items.all()
        )
        return total_cost - total_cost * (self.discount / Decimal(100))


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
