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

    def __init__(self, *args, **kwargs):
        super(IncidenciaForm, self).__init__(*args, **kwargs)
        self.fields['incidencia'].queryset = Incidencia.objects.filter(estatus__in='1')


class CitaIncidenciaAlForm(forms.ModelForm):
    class Meta:
        model = CitaIncidencia
        fields = '__all__'
        exclude = ['estatus']

    def __init__(self, *args, **kwargs):
        grado = kwargs.pop('grado')
        grupo = kwargs.pop('grupo')
        pk = kwargs.pop('pk')
        super(CitaIncidenciaAlForm, self).__init__(*args, **kwargs)
        print(grado)
        self.fields['incidencia'].queryset = Incidencia.objects.filter(incidenciaalumno__alumno__grado=grado,
                                                                       incidenciaalumno__alumno__grupo=grupo,
                                                                       estatus__in='1')
        self.fields['cita'].queryset = Cita.objects.filter(id_cita=pk)
