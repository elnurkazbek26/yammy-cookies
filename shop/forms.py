from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'email', 'address', 'quantity', 'comment']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя', 'class': 'form-input'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+996 XXX XXX XXX', 'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@mail.com', 'class': 'form-input'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3, 'placeholder': 'Город, улица, дом, квартира', 'class': 'form-input'
            }),
            'quantity': forms.NumberInput(attrs={
                'min': 1, 'max': 99, 'class': 'form-input'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 3, 'placeholder': 'Пожелания к заказу (необязательно)', 'class': 'form-input'
            }),
        }
        labels = {
            'customer_name': 'Ваше имя',
            'phone': 'Телефон',
            'email': 'Email (необязательно)',
            'address': 'Адрес доставки',
            'quantity': 'Количество',
            'comment': 'Комментарий',
        }
