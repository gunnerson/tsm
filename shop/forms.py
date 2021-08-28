from django import forms

from .models import Order, JobItem
from invent.mixins import FormMixin


class OrderForm(FormMixin):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'opened': forms.DateInput(attrs={'type': 'date'}),
            'closed': forms.DateInput(attrs={'type': 'date'}),
            'jobs': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, is_create=None, **kwargs):
        super().__init__(*args, **kwargs)
        if is_create:
            self.fields['closed'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        truck = cleaned_data.get("truck")
        trailer = cleaned_data.get("trailer")
        if (truck and trailer) or (not truck and not trailer):
            msg = forms.ValidationError(('Select either truck or trailer'),
                                        code='invalid')
            self.add_error('trailer', msg)


class JobItemForm(FormMixin):
    class Meta:
        model = JobItem
        fields = '__all__'
