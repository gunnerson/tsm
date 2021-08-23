from django import forms

from .models import Truck, Trailer, Company, Driver, PasswordGroup


class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        exclude = ('account',)
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
        exclude = ('account', )
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


class TruckSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        option = super().create_option(name, value, label, selected, index,
                                       subindex, attrs)
        object_id = option['value'].__str__()
        if object_id:
            ob = Truck.objects.get(id=object_id)
            try:
                ob.driver
                option['attrs']['class'] = 'choice_taken'
            except Truck.driver.RelatedObjectDoesNotExist:
                pass
        return option


class TrailerSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        option = super().create_option(name, value, label, selected, index,
                                       subindex, attrs)
        object_id = option['value'].__str__()
        if object_id:
            obj = Trailer.objects.get(id=object_id)
            try:
                obj.driver
                option['attrs']['class'] = 'choice_taken'
            except Trailer.driver.RelatedObjectDoesNotExist:
                pass
        return option


class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver
        exclude = ('account',)
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
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields["truck"] = forms.ModelChoiceField(
            queryset=Truck.objects.filter(account=self.account),
            widget=TruckSelect,
            required=False,
        )
        self.fields["trailer"] = forms.ModelChoiceField(
            queryset=Trailer.objects.filter(account=self.account),
            widget=TrailerSelect,
            required=False,
        )
        self.fields["home_address"].widget.attrs.update({'rows': 1})
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'formset_field'})


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('account',)
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
        exclude = ('account',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
