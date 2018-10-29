from django import forms
from .models import *


class CitaOtroForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        exclude = ['estatus']


class CitaIncidenciaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        exclude = ['estatus']


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = CitaIncidencia
        fields = ['incidencia']
        print(fields)
        print("holaaaa")

