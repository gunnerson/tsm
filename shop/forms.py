from django import forms

from .models import Order, Job, Part, OrderJob, OrderPart, Purchase, PurchaseItem
from .mixins import OrderSelect
from invent.mixins import FormMixin, FormSetMixin


class OrderForm(FormMixin):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'opened': forms.DateInput(attrs={'type': 'date'}),
            'closed': forms.DateInput(attrs={'type': 'date'}),
            'jobs': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, is_create=None, **kwargs):
        super().__init__(*args, **kwargs)
        if is_create:
            self.fields['closed'].disabled = True
        else:
            self.fields['truck'].disabled = True
            self.fields['trailer'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        truck = cleaned_data.get("truck")
        trailer = cleaned_data.get("trailer")
        if (truck and trailer) or (not truck and not trailer):
            msg = forms.ValidationError(('Select either truck or trailer'),
                                        code='invalid')
            self.add_error('trailer', msg)


class JobForm(FormSetMixin):
    class Meta:
        model = Job
        fields = '__all__'


class OrderJobForm(forms.ModelForm):
    class Meta:
        model = OrderJob
        fields = '__all__'

    def __init__(self, *args, exclude=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["job"] = forms.ModelChoiceField(
            queryset=Job.objects.all(),
            widget=OrderSelect(exclude=exclude),
        )
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class OrderPartForm(forms.ModelForm):
    class Meta:
        model = OrderPart
        fields = '__all__'

    def __init__(self, *args, parts=None, exclude=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["part"] = forms.ModelChoiceField(
            queryset=parts,
            widget=OrderSelect(exclude=exclude),
        )
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class PartForm(FormSetMixin):
    class Meta:
        model = Part
        fields = '__all__'


class PurchaseForm(FormMixin):
    class Meta:
        model = Purchase
        fields = '__all__'


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = '__all__'

    def __init__(self, *args, exclude=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["part"] = forms.ModelChoiceField(
            queryset=Part.objects.all(),
            widget=OrderSelect(exclude=exclude),
        )
        self.fields["price"].widget.attrs.update({'placeholder': 'Price'})
        self.fields["amount"].widget.attrs.update({'placeholder': 'Amount'})
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
