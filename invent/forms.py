from django import forms
from datetime import date
from django.db.models import Q

from .models import Truck, Trailer
from contacts.models import Company
from contacts.models import Driver


class TruckForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        required=False,
    )
    owner = forms.ModelChoiceField(
        queryset=Company.objects.filter(Q(group='OU') | Q(group='LO')),
        required=False,
    )
    insurer = forms.ModelChoiceField(
        queryset=Company.objects.filter(group='IN'),
        required=False,
    )

    class Meta:
        model = Truck
        exclude = ('account',)
        widgets = {
            'registration': forms.DateInput(attrs={'type': 'date'}),
            'insurance': forms.DateInput(attrs={'type': 'date'}),
            'inspection': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update')
        super().__init__(*args, **kwargs)
        if self.is_update:
            self.fields['fleet_number'].disabled = True
        else:
            self.fields["driver"].widget = forms.HiddenInput()
            self.fields["driver"].label = ''
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class TrailerForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        required=False,
    )

    class Meta:
        model = Trailer
        exclude = ('account',)

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update')
        super().__init__(*args, **kwargs)
        if self.is_update:
            self.fields['fleet_number'].disabled = True
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
