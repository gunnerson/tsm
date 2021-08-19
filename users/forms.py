from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User, PreferenceList, Account


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
    )
    new_account = forms.CharField(max_length=36, required=False)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        cd_account = cleaned_data.get("account")
        cd_new_account = cleaned_data.get("new_account")
        if cd_account is None and cd_new_account == '':
            msg = forms.ValidationError(
                ('Either select an existing account or specify name for a new account'),
                code='invalid')
            self.add_error('new_account', msg)
        if cd_account is not None and cd_new_account != '':
            msg = forms.ValidationError(
                ('Either select an existing account or specify name for a new account, not both at the same time'),
                code='invalid')
            self.add_error('new_account', msg)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


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


class PreferenceListForm(forms.ModelForm):
    first_name = forms.CharField(max_length=24, required=False)
    last_name = forms.CharField(max_length=24, required=False)

    class Meta:
        model = PreferenceList
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


class UserGroupsForm(forms.Form):
    user = forms.CharField(max_length=24, required=False)
    last_name = forms.CharField(max_length=24, required=False)

    class Meta:
        model = PreferenceList
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
