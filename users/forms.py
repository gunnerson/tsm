from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User, Profile


class UserCreationForm(forms.ModelForm):
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


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=24, required=False)
    last_name = forms.CharField(max_length=24, required=False)

    class Meta:
        model = Profile
        exclude = ('user', 'level',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})


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
