from django import forms

from .models import Order, Job, Part, OrderJob, OrderPart, Purchase, \
    PurchaseItem, Balance, Inspection
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
            'comments': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(
            self, *args, is_create=None, trucks=None, trailers=None, **kwargs):
        super().__init__(*args, **kwargs)
        if is_create:
            self.fields['closed'].disabled = True
            if trucks:
                self.fields['truck'].queryset = trucks
                self.fields['truck'].widget.attrs.update(
                    {'class': 'form_field'})
            if trailers:
                self.fields['trailer'].queryset = trailers
                self.fields['trailer'].widget.attrs.update(
                    {'class': 'form_field'})
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].disabled = True
        if self.instance.track:
            self.fields["part_number"].widget.attrs.update(
                {'style': 'color:red'}
            )


class PurchaseForm(FormMixin):
    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, is_create=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_create:
            self.fields['vendor'].disabled = True
            self.fields['date'].disabled = True


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
        self.fields["price"].widget.attrs.update(
            {'placeholder': 'Price', 'style': 'width:12ch'})
        self.fields["amount"].widget.attrs.update(
            {'placeholder': 'Amount', 'style': 'width:12ch'})
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class BalanceForm(FormSetMixin):
    class Meta:
        model = Balance
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.TextInput(attrs={'size': 60}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.instance.total > 0:
                for f in self.fields:
                    self.fields[f].widget.attrs.update(
                        {'class': 'formset_field income'})
            else:
                for f in self.fields:
                    self.fields[f].widget.attrs.update(
                        {'class': 'formset_field expenses'})
        except TypeError:
            pass


class InspectionForm(FormMixin):
    class Meta:
        model = Inspection
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, is_create=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_create:
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


class OrderTimeForm(forms.Form):
    order = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, order=None, mechanic=None, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Order.objects.filter(closed=None)
        # taken_ids = []
        # for q in qs:
        #     if q.taken and (q.mechanic != mechanic):
        #         taken_ids.append(q.id)
        # qs = qs.exclude(id__in=taken_ids)
        self.fields['order'].queryset = qs
        if order:
            self.fields['order'].initial = order
            self.fields['order'].disabled = True
