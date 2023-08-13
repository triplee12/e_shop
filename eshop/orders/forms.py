"""Order forms."""

from django import forms
from localflavor.us.forms import USZipCodeField
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Order form."""

    class Meta:
        """Order form meta data."""

        postal_code = USZipCodeField()

        class Meta:
            """Order meta details."""

            model = Order
            fields = [
                'first_name', 'last_name',
                'email', 'address',
                'postal_code', 'city'
            ]
