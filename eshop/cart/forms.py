"""Cart form."""
from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 30)]


class CartAddProductForm(forms.Form):
    """Add product to cart."""

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
