"""Coupon forms."""

from django import forms


class CouponApplyForm(forms.Form):
    """Coupon apply form."""

    code = forms.CharField()
