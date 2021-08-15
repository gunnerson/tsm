from django import forms
from datetime import date

from .models import Truck, Trailer
from contacts.models import Driver


def year_choices():
    choices = []
    default = ('', '----')
    choices.append(default)
    for r in range(1990, date.today().year + 1):
        c = (r, r)
        choices.append(c)
    return choices


class TruckForm(forms.ModelForm):
    year = forms.ChoiceField(
        choices=year_choices,
        label='Year',
        required=False,
    )
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        required=False,
    )

    class Meta:
        model = Truck
        fields = '__all__'
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
            self.fields['company'].disabled = True
        else:
            self.fields["driver"].widget = forms.HiddenInput()
            self.fields["driver"].label = ''
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class TrailerForm(forms.ModelForm):
    year_made = forms.ChoiceField(
        choices=year_choices,
        required=False,
        label='Year',
    )
    driver = forms.ModelChoiceField(
        queryset=Driver.objects.all(),
        required=False,
    )

    class Meta:
        model = Trailer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update')
        super().__init__(*args, **kwargs)
        if self.is_update:
            self.fields['fleet_number'].disabled = True
            self.fields['company'].disabled = True
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
