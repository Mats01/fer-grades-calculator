import re

from .models import Komponenta, KomponentaBodovi, Predmet
from django import forms
from django.core.exceptions import ValidationError


class StudentKomponentaBodoviForm(forms.ModelForm):
    class Meta:
        model = KomponentaBodovi

        fields = ['points_collected', 'komponenta', 'description', 'predmet', ]
        widgets = {'predmet': forms.HiddenInput(), }

    def __init__(self, *args, **kwargs):
        # instance_predmet = kwargs.pop('instance_predmet', None)

        super(StudentKomponentaBodoviForm, self).__init__(*args, **kwargs)

        self.fields['points_collected'].widget.attrs['class'] = 'intable_input'
        self.fields['komponenta'].widget.attrs['class'] = 'intable_input'
        self.fields['description'].widget.attrs['class'] = 'intable_input'

        if kwargs:
            predmet = kwargs['initial']['predmet'].predmet

            self.fields['komponenta'].queryset = Komponenta.objects.filter(
                predmet=predmet,
            )


class EmailAuthForm(forms.Form):
    email = forms.EmailField(
        label='Unesite svoju fer emial adresu',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'ime.prezime@fer.hr'}))

    def clean_email(self):
        data = self.cleaned_data['email']
        # if "matej.butkovic@fer.hr" not in data:
        #     raise ValidationError("Dana email adresa nije FER emial adresa")
        if not re.match("^[a-z]+.[a-z]+[0-9]*@fer.hr$", data):
            raise ValidationError("Dana email adresa nije FER emial adresa")

        return data


class CodeAuthForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    code = forms.CharField(
        label='Unesite kod', max_length=6,
        widget=forms.TextInput(attrs={'placeholder': '6 digit code'}))

    def clean_email(self):
        data = self.cleaned_data['email']
        # if "matej.butkovic@fer.hr" not in data:
        #     raise ValidationError("Dana email adresa nije FER emial adresa")
        if not re.match("^[a-z]+.[a-z]+[0-9]*@fer.hr$", data):
            raise ValidationError("Dana email adresa nije FER emial adresa")

        return data
