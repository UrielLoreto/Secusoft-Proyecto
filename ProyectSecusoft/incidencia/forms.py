from django import forms
from .models import *


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = '__all__'
        exclude = ['estatus']
        labels = {'incidencia': 'Tipo de incidencia'}


class IncidenciaTipoForm(forms.ModelForm):
    class Meta:
        model = TipoIndicencia
        fields = '__all__'


class IncidenciaAlForm(forms.ModelForm):
    class Meta:
        model = IncidenciaAlumno
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        grado = kwargs.pop('grado')
        grupo = kwargs.pop('grupo')
        pk = kwargs.pop('pk')
        super(IncidenciaAlForm, self).__init__(*args, **kwargs)
        self.fields['alumno'].queryset = Alumno.objects.filter(grado=grado, grupo=grupo)
        self.fields['incidencia'].queryset = Incidencia.objects.filter(id_incidencia=pk)


class IndicenciaDocenteForm(forms.ModelForm):
    class Meta:
        model = IncidenciaDocente
        exclude = ['incidencia', 'docente']


class UploadFileForm(forms.Form):
    file = forms.FileField()
