from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'order_details', 'total_price']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter your name')
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+374 12 34 56 78',
                'type': 'tel'
            }),
            'order_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Describe your order (e.g.: Classic shawarma x2, Cola x1)')
            }),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'customer_name': _('Your Name'),
            'phone': _('Phone'),
            'order_details': _('Order Details'),
            'total_price': _('Total Price'),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            cleaned_phone = ''.join(c for c in phone if c.isdigit() or c == '+')
            if len(cleaned_phone) < 10:
                raise forms.ValidationError(_('Phone number must contain at least 10 digits'))
            return cleaned_phone
        return phone
    
    def clean_total_price(self):
        total_price = self.cleaned_data.get('total_price')
        if total_price is not None and total_price < 0:
            raise forms.ValidationError(_('Price cannot be negative'))
        return total_price

