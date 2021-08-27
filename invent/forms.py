from django import forms

from .mixins import VehicleSelect, FormMixin, FormSetMixin
from .models import Truck, Trailer, Company, Driver, PasswordGroup


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


class DriverForm(FormSetMixin):
    class Meta:
        model = Driver
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'cdl_exp_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_exp_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'term_date': forms.DateInput(attrs={'type': 'date'}),
            'last_mvr': forms.DateInput(attrs={'type': 'date'}),
            'last_clearinghouse': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["truck"] = forms.ModelChoiceField(
            queryset=Truck.objects.all(),
            widget=VehicleSelect(model=Truck),
            required=False,
        )
        self.fields["trailer"] = forms.ModelChoiceField(
            queryset=Trailer.objects.all(),
            widget=VehicleSelect(model=Trailer),
            required=False,
        )
        self.fields["truck"].widget.attrs.update({'class': 'formset_field'})
        self.fields["trailer"].widget.attrs.update({'class': 'formset_field'})
        self.fields["home_address"].widget.attrs.update({'rows': 1})


class CompanyForm(FormSetMixin):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 1})
        }


class PasswordGroupForm(FormMixin):
    class Meta:
        model = PasswordGroup
        fields = '__all__'

