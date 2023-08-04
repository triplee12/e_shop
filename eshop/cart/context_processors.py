"""Cart context processor."""

from .cart import Cart


def cart(request):
    """Cart context processor."""
    return {"cart": Cart(request)}
