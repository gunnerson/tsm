from django import forms

from .models import Driver, Company, PasswordGroup
from invent.models import Truck, Trailer


class TruckSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        itera = option['value'].__str__()
        if itera != '':
            ob = Truck.objects.get(id=itera)
            try:
                t = ob.driver
                option['attrs']['class'] = 'choice_taken'
            except Truck.driver.RelatedObjectDoesNotExist:
                pass
        return option


class TrailerSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        itera = option['value'].__str__()
        if itera != '':
            ob = Trailer.objects.get(id=itera)
            try:
                t = ob.driver
                option['attrs']['class'] = 'choice_taken'
            except Trailer.driver.RelatedObjectDoesNotExist:
                pass
        return option


class DriverForm(forms.ModelForm):
    truck = forms.ModelChoiceField(
        queryset=Truck.objects.all(),
        required=False,
        widget=TruckSelect,
    )
    trailer = forms.ModelChoiceField(
        queryset=Trailer.objects.all(),
        required=False,
        widget=TrailerSelect,
    )

    class Meta:
        model = Driver
        exclude = ('truck', 'trailer', )

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
        widgets = {'comments': forms.Textarea(attrs={'cols': 80})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class PasswordGroupForm(forms.ModelForm):
    class Meta:
        model = PasswordGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
