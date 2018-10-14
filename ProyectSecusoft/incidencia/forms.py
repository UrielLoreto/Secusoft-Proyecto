from django import forms
from .models import *


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = '__all__'
        exclude = ['estatus']


class IncidenciaAlForm(forms.ModelForm):
    class Meta:
        model = IncidenciaAlumno
        fields = ['alumno']


class IndicenciaDocenteForm(forms.ModelForm):
    class Meta:
        model = IncidenciaDocente
        exclude = ['incidencia', 'docente']

