"""Product recommender."""

import redis
from django.conf import settings
from .models import Product

# connent to redis
r_conn = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


class Recommender(object):
    """Recommend products."""

    def get_product_key(self, id):
        """Get the product key."""
        return f'product:{id}:purchase_with'

    def product_bought(self, products):
        """Product bought."""
        product_ids = [product.id for product in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r_conn.zincrby(
                        self.get_product_key(product_id),
                        1, with_id
                    )

    def suggest_products_for(self, products, max_results=6):
        """
        Suggests products to users based on their purchases.

        Args:
            products: A list of products to get recommendations for.
                It can contain one or more products.
            max_results: Maximum number of recommendations to return.

        Returns:
            list: A list of recommendations
        """
        product_ids = [product.id for product in products]
        if len(products) == 1:
            # only 1 product
            suggestions = r_conn.zrange(
                self.get_product_key(products[0]),
                0, -1,
                desc=True
            )[:max_results]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r_conn.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r_conn.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r_conn.zrange(
                tmp_key, 0, -1, desc=True
            )[:max_results]
            # remove the temporary key
            r_conn.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(
            id__in=suggested_products_ids
        ))
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )
        return suggested_products

    def clear_purchases(self):
        """Clear all pending purchases."""
        for id in Product.objects.values_list('id', flat=True):
            r_conn.delete(self.get_product_key(id))
