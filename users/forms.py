from django import forms

from .models import PreferenceList


class PreferenceListForm(forms.ModelForm):
    class Meta:
        model = PreferenceList
        exclude = ('profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form_field'})
