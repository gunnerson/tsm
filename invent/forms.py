from django import forms

from .mixins import VehicleSelect
from .models import Truck, Trailer, Company, Driver, PasswordGroup


class TruckForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'formset_field'})


class TrailerForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'formset_field'})


class DriverForm(forms.ModelForm):
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
        db_name = kwargs.pop('db_name')
        super().__init__(*args, **kwargs)
        self.fields["truck"] = forms.ModelChoiceField(
            queryset=Truck.objects.using(db_name).all(),
            widget=VehicleSelect(model=Truck, db_name=db_name),
            required=False,
        )
        self.fields["trailer"] = forms.ModelChoiceField(
            queryset=Trailer.objects.using(db_name).all(),
            widget=VehicleSelect(model=Trailer, db_name=db_name),
            required=False,
        )
        self.fields["home_address"].widget.attrs.update({'rows': 1})
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'formset_field'})


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 1})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'formset_field'})


class PasswordGroupForm(forms.ModelForm):
    class Meta:
        model = PasswordGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
