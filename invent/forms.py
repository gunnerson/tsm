from django import forms

from .mixins import VehicleSelect, FormMixin, FormSetMixin
from .models import Truck, Trailer, Company


class TruckForm(FormSetMixin):
    class Meta:
        model = Truck
        fields = '__all__'
        widgets = {
            'registration': forms.DateInput(attrs={'type': 'date'}),
            'insurance': forms.DateInput(attrs={'type': 'date'}),
            'inspection': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'term_date': forms.DateInput(attrs={'type': 'date'}),
            'last_pm_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TrailerForm(FormSetMixin):
    class Meta:
        model = Trailer
        fields = '__all__'
        widgets = {
            'registration': forms.DateInput(attrs={'type': 'date'}),
            'insurance': forms.DateInput(attrs={'type': 'date'}),
            'inspection': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'term_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CompanyForm(FormSetMixin):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 1})
        }
