import re

from .models import KomponentaBodovi
from django import forms
from django.core.exceptions import ValidationError


class StudentKomponentaBodoviForm(forms.ModelForm):
    class Meta:
        model = KomponentaBodovi
        fields = ['points_collected', ]


class EmailAuthForm(forms.Form):
    email = forms.EmailField(
        label='Unesite svoju fer emial adresu', max_length=100)

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
        label='Unesite kod', max_length=6)

    def clean_email(self):
        data = self.cleaned_data['email']
        # if "matej.butkovic@fer.hr" not in data:
        #     raise ValidationError("Dana email adresa nije FER emial adresa")
        if not re.match("^[a-z]+.[a-z]+[0-9]*@fer.hr$", data):
            raise ValidationError("Dana email adresa nije FER emial adresa")

        return data
            