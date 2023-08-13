"""Coupon forms."""

from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    """Coupon apply form."""

    code = forms.CharField(label=_('Coupon'))
