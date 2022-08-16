from django import forms

from .models import Order, Job, Part, OrderJob, OrderPart, Purchase, \
    PurchaseItem, Balance, PartPlace, PartType, Mechanic, Shelf, ShelfGroup, \
    Core, CoreReturn
from .mixins import OrderSelect
from invent.models import Truck, Trailer
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
        self.fields['mechanic'].queryset = Mechanic.objects.filter(active=True)

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
        # if self["part"].value() is not None:
        #     self.fields["part"].widget.attrs["readonly"] = True
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class PartTypeForm(FormSetMixin):
    class Meta:
        model = PartType
        fields = '__all__'


class PartForm(FormSetMixin):
    class Meta:
        model = Part
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].disabled = True
        # if self.instance.track:
        #     if self.instance.stock == 0:
        #         self.fields["part_number"].widget.attrs.update(
        #             {'style': 'color:red'}
        #         )
        #     elif self.instance.stock == 1:
        #         self.fields["part_number"].widget.attrs.update(
        #             {'style': 'color:orange'}
        #         )


class PartUpdateForm(FormMixin):
    class Meta:
        model = Part
        fields = '__all__'


class PartPlaceForm(FormSetMixin):
    class Meta:
        model = PartPlace
        fields = '__all__'

    def __init__(self, *args, exclude=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["part"] = forms.ModelChoiceField(
            queryset=Part.objects.all(),
            widget=OrderSelect(exclude=exclude),
            required=False,
        )
        for f in self.fields:
            self.fields[f].widget.attrs.update({'style': 'border:0'})


class PurchaseForm(FormMixin):
    truck = forms.ModelChoiceField(
        queryset=Truck.objects.all(),
        required=False,
    )
    trailer = forms.ModelChoiceField(
        queryset=Trailer.objects.all(),
        required=False,
    )

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


class ShelfForm(FormMixin):
    class Meta:
        model = Shelf
        fields = '__all__'

    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].initial = group
        self.fields["group"].disabled = True
        qs = Part.objects.filter(part_type__in=group.part_type.all())
        self.fields["part"].queryset = qs


class ShelfGroupForm(FormMixin):
    class Meta:
        model = ShelfGroup
        fields = ('part_type',)


class CoreForm(FormMixin):

    class Meta:
        model = Core
        fields = ('part', 'amount', 'price')

    def __init__(self, *args, parts=None, exclude=None, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields["part"].queryset = parts
            self.fields["part"].widget = OrderSelect(exclude=exclude)
        except KeyError:
            pass


class CoreReturnForm(FormMixin):

    class Meta:
        model = CoreReturn
        fields = '__all__'
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), }

    def __init__(self, *args, cores=None, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['core'].queryset = cores
        except KeyError:
            pass

    def clean(self):
        cleaned_data = super().clean()
        core = cleaned_data.get("core")
        buy_amount = core.part.amount
        return_amount = cleaned_data.get("amount")
        if return_amount > buy_amount:
            msg = forms.ValidationError(('Return amount exceeds purchase amount'),
                                        code='invalid')
            self.add_error('amount', msg)
