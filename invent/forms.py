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
        try:
            self.is_view = kwargs.pop('is_view')
        except KeyError:
            self.is_view = False
        super().__init__(*args, **kwargs)
        for f in self.fields:
            if self.is_view:
                self.fields[f].widget.attrs.update({'class': 'form_field'})
            else:
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
        try:
            self.is_view = kwargs.pop('is_view')
        except KeyError:
            self.is_view = False
        super().__init__(*args, **kwargs)
        for f in self.fields:
            if self.is_view:
                self.fields[f].widget.attrs.update({'class': 'form_field'})
            else:
                self.fields[f].widget.attrs.update({'class': 'formset_field'})


class TruckSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        option = super().create_option(name, value, label, selected, index,
                                       subindex, attrs)
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
    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        option = super().create_option(name, value, label, selected, index,
                                       subindex, attrs)
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
    # truck = forms.ModelChoiceField(
    #     queryset=Truck.objects.all(),
    #     required=False,
    #     widget=TruckSelect,
    # )
    # trailer = forms.ModelChoiceField(
    #     queryset=Trailer.objects.all(),
    #     required=False,
    #     widget=TrailerSelect,
    # )

    class Meta:
        model = Driver
        exclude = ('account',)

    def __init__(self, *args, **kwargs):
        try:
            self.is_view = kwargs.pop('is_view')
        except KeyError:
            self.is_view = False
        super().__init__(*args, **kwargs)
        self.fields["home_address"].widget.attrs.update({'rows': 1})
        # self.fields["trailer"].widget = TrailerSelect
        # self.fields["trailer"].widget = TrailerSelect
        for f in self.fields:
            if self.is_view:
                self.fields[f].widget.attrs.update({'class': 'form_field'})
            else:
                self.fields[f].widget.attrs.update({'class': 'formset_field'})

    # def __init__(self, *args, **kwargs):
    #     self.is_update = kwargs.pop('is_update')
    #     super().__init__(*args, **kwargs)
    #     if not self.is_update:
    #         self.fields["truck"].widget = forms.HiddenInput()
    #         self.fields["trailer"].widget = forms.HiddenInput()
    #         self.fields["truck"].label = ''
    #         self.fields["trailer"].label = ''
    #     for f in self.fields:
    #         self.fields[f].widget.attrs.update({'class': 'form_field'})


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('account',)
        widgets = {'comments': forms.Textarea(attrs={'cols': 80})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class PasswordGroupForm(forms.ModelForm):
    class Meta:
        model = PasswordGroup
        exclude = ('account',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
