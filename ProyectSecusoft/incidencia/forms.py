from django import forms
from .models import *


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = '__all__'


class IncidenciaAlForm(forms.ModelForm):
    class Meta:
        model = IncidenciaAlumno
        fields = '__all__'


class IndicenciaDocenteForm(forms.ModelForm):
    class Meta:
        model = IncidenciaDocente
        fields = '__all__'
