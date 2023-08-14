"""Cart views."""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shops.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shops.recommender import Recommender


@require_POST
def cart_add(request, product_id: int):
    """
    Cart product to the cart view.

    Args:
        product_id (int): unique identifier of the product
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Remove product from cart.

    Args:
        product_id (int): product id to the product to be removed
    """
    cart = Cart(request)
    product = get_object_or_404(
        Product, id=product_id
    )
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    """Cart detail view."""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )
    coupon_apply_form = CouponApplyForm()
    recommend = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = recommend.suggest_products_for(
        cart_products,
        max_results=4
    )
    return render(
        request, 'cart/detail.html',
        {
            'cart': cart,
            'coupon_apply_form': coupon_apply_form,
            'recommended_products': recommended_products
        }
    )
