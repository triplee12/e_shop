"""Cart session."""

from decimal import Decimal
from django.conf import settings
from shops.models import Product
from coupons.models import Coupon


class Cart(object):
    """Cart session."""

    def __init__(self, request):
        """Initialize the Cart instance."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity: int = 1, override_quantity: bool = False):
        """
        Add a product to the cart or update its quantity.

        Args:
            product: product instance to add in the cart
            quantity (int): quantity of the product added
            override_quantity (bool): override quantity of the product
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            self.save()

    def save(self):
        """Save the session."""
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.

        Args:
            product: the product instance to be removed
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart.

        And update the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(
            id__in=product_ids
        )
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart.

        Returns:
            int: total number of all the items
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total price of the products.

        Return:
            Decimal: the total amount of the products
        """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Clear cart from session."""
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """Coupon method."""
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """Get discount."""
        if self.coupon:
            return (
                self.coupon.discount / Decimal(100)
            ) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """Get total price after discount."""
        return self.get_total_price() - self.get_discount()
