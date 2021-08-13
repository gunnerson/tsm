from django import forms

from .models import Driver, Company
from invent.models import Truck, Trailer


class DriverForm(forms.ModelForm):
    truck = forms.ModelChoiceField(
        queryset=Truck.objects.all(),
        required=False,
    )
    trailer = forms.ModelChoiceField(
        queryset=Trailer.objects.all(),
        required=False,
    )
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'phone_number',]

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update')
        super().__init__(*args, **kwargs)
        if not self.is_update:
            self.fields["truck"].widget = forms.HiddenInput()
            self.fields["trailer"].widget = forms.HiddenInput()
            self.fields["truck"].label = ''
            self.fields["trailer"].label = ''
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
