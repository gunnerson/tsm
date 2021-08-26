from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('account',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})

