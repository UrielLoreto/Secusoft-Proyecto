from django import forms
from .models import *


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = '__all__'


class MateriaDocenteForm(forms.ModelForm):
    class Meta:
        model = MateriaDocente
        fields = '__all__'
        exclude = ['materia']