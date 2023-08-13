"""Shop admin registration."""

from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """Category admin registration form."""

    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        """Get all prepopulated fields."""
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    """Product admin registration form."""

    list_display = [
        'name', 'slug', 'price',
        'available', 'created_at', 'updated_at'
    ]
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'available']

    def get_prepopulated_fields(self, request, obj=None):
        """Get all prepopulated fields."""
        return {'slug': ('name',)}
