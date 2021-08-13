from django import forms
from datetime import date

from .models import Truck, Trailer


def year_choices():
    return [(r, r) for r in range(1990, date.today().year + 1)]


class TruckForm(forms.ModelForm):
    year_made = forms.ChoiceField(
        choices=year_choices,
        initial=date.today().year,
        label='Year',
    )

    class Meta:
        model = Truck
        fields = '__all__'
        labels = {
            'fleet_number': 'Fleet number',
            'lic_plate': 'License plate',
            'make': 'Make',
            'model': 'Model',
            'vin': 'VIN',
            'mileage': 'Mileage',
            'engine': 'Engine manufacturer',
            'engine_model': 'Engine model',
            'engine_number': 'Model',
            'reg_exp': 'Registration expiration date',
            'ins_exp': 'Insurance expiration date',
            'is_active': 'Active',
        }
        widgets = {
            'reg_exp': forms.DateInput(attrs={'type': 'date'}),
            'ins_exp': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class TrailerForm(forms.ModelForm):
    year_made = forms.ChoiceField(
        choices=year_choices,
        initial=date.today().year,
        label='Year',
    )

    class Meta:
        model = Trailer
        fields = '__all__'
        labels = {
            'fleet_number': 'Fleet number',
            'lic_plate': 'License plate',
            'make': 'Manufacturer',
            'vin': 'VIN',
            'is_active': 'Active',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
