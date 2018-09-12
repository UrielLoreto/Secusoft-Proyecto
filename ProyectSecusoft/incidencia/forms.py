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


class IncidenciaTipoForm(forms.ModelForm):
    class Meta:
        model = TipoIndicencia
        fields = '__all__'
