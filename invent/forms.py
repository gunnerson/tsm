from django import forms
from datetime import date
# from django.core.validators import RegexValidator

from .models import Truck, Trailer

# alphanumeric = RegexValidator(
#     r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        exclude = ('account',)
        widgets = {
            'registration': forms.DateInput(attrs={'type': 'date'}),
            'insurance': forms.DateInput(attrs={'type': 'date'}),
            'inspection': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        try:
            self.is_view = kwargs.pop('is_view')
        except KeyError:
            self.is_view = False
        super().__init__(*args, **kwargs)
        if self.is_view:
            for f in self.fields:
                self.fields[f].widget.attrs.update({'class': 'form_field'})
        else:
            for f in self.fields:
                self.fields[f].widget.attrs.update({'class': 'formset_field'})


class TrailerForm(forms.ModelForm):
    class Meta:
        model = Trailer
        exclude = ('account', )
        widgets = {
            'registration': forms.DateInput(attrs={'type': 'date'}),
            'insurance': forms.DateInput(attrs={'type': 'date'}),
            'inspection': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        try:
            self.is_view = kwargs.pop('is_view')
        except KeyError:
            self.is_view = False
        super().__init__(*args, **kwargs)
        if self.is_view:
            for f in self.fields:
                self.fields[f].widget.attrs.update({'class': 'form_field'})
        else:
            for f in self.fields:
                self.fields[f].widget.attrs.update({'class': 'formset_field'})


class BaseTruckFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        account = self.request.user.profile.account
        self.queryset = Truck.objects.filter(account=account)


class BaseTrailerFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        account = self.request.user.profile.account
        self.queryset = Trailer.objects.filter(account=account)
