"""Shop model module."""
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Category model."""

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        """Meta information."""

        ordering = ('name',)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        """String representation of a category."""
        return f"{self.name}"

    def get_absolute_url(self):
        """Get a particular category."""
        return reverse(
            "shops:product_list_by_category",
            args=[self.slug]
        )


class Product(models.Model):
    """Product model."""

    category = models.ForeignKey(
        Category, related_name="products",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta information."""

        ordering = ("name",)
        index_together = (("id", "slug"),)

    def __str__(self) -> str:
        """String representation of the product."""
        return f"{self.name}"

    def get_absolute_url(self):
        """Get a particular product."""
        return reverse(
            "shops:product_detail",
            args=[self.id, self.slug]
        )
