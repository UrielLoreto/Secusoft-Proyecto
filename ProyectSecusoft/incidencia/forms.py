from django import forms
from .models import Incidencia


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = (
            'id_incidencia',
            'fecha_incidencia',
            'asunto',
            'estatus',
            'observaciones',
            'tipo',
        )
