"""Shop views."""

from django.shortcuts import get_object_or_404, render
from cart.forms import CartAddProductForm
from .models import Category, Product
from .recommender import Recommender


def product_list(request, category_slug=None):
    """
    Retrieve list of products.

    Args:
        category_slug (str): retrieve products by category
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug
        )
        products = products.filter(category=category)
    context = {
        "category": category,
        "categories": categories,
        "products": products
    }
    return render(
        request, "shops/product/list.html",
        context=context
    )


def product_detail(request, id, slug):
    """
    Retrieve a product by the given id and slug.

    Args:
        id (int): unique identifier of the product
        slug (str): product slug
    """
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product, id=id,
        translations__language_code=language,
        translations__slug=slug,
        available=True
    )
    cart_product_form = CartAddProductForm()
    recommend = Recommender()
    recommended_products = recommend.suggest_products_for(
        [product], 4
    )
    return render(
        request, "shops/product/detail.html",
        {
            "product": product,
            'cart_product_form': cart_product_form,
            'recommended_products': recommended_products
        }
    )
