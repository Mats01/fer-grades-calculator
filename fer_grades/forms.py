from .models import KomponentaBodovi
from django.forms import ModelForm


class StudentKomponentaBodoviForm(ModelForm):
    class Meta:
        model = KomponentaBodovi
        fields = ['points_collected', ]
