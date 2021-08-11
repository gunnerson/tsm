from django import forms

from .models import Truck


class TruckCreateForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = [
            'fleet_number',
            'lic_plate',
            'make',
            'model',
        ]
        labels = {
            'fleet_number': 'Fleet Number',
            'lic_plate': 'License Plate',
            'make': 'Make',
            'model': 'Model',
        }


class TruckUpdateForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = [
            'fleet_number',
            'lic_plate',
            'make',
            'model',
        ]
        labels = {
            'fleet_number': 'Fleet Number',
            'lic_plate': 'License Plate',
            'make': 'Make',
            'model': 'Model',
        }
