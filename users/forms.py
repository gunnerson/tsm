from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from datetime import datetime

from .models import User, Profile, AccountVar
from shop.models import Mechanic
from .mixins import FormMixin


class UserCreationForm(FormMixin):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password1")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password1", error)


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        exclude = ('password',)


class ProfileForm(FormMixin):
    first_name = forms.CharField(max_length=24, required=False)
    last_name = forms.CharField(max_length=24, required=False)

    class Meta:
        model = Profile
        exclude = ('user', 'level', )


class UserLevelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'level',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].disabled = True
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'formset_field'})
            self.fields[f].widget.attrs.update({'style': 'font-size: 1rem'})


class PunchCardForm(forms.Form):
    mechanic = forms.ModelChoiceField(
        queryset=Mechanic.objects.filter(active=True), empty_label=None)
    week_of = forms.DateField(
        initial=datetime.today(),
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, mechanic=None, level=None, week_of=None, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update(
                {'class': 'form_field filter_form'})
        if mechanic:
            self.fields['mechanic'].initial = mechanic
        if week_of:
            self.fields['week_of'].initial = week_of
        if level != 'A':
            self.fields['mechanic'].disabled = True


class AccountVarForm(FormMixin):
    class Meta:
        model = AccountVar
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].disabled = True
