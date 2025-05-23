from .models import Order
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'phone', 'address', 'postal_code'
        ]


class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(max_length=11)
