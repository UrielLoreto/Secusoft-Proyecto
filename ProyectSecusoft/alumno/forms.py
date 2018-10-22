from django import forms
from .models import *


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        exclude = ['alumno']
        labels = {'grado': 'Grado:',
                  'grupo': 'Grupo:'}
    matricula = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '15110167',
            'require': 'true'}),
        label='Matricula:')


class AlumnoActForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        exclude = ['alumno', 'matricula']
        labels = {'grado': 'Grado:',
                  'grupo': 'Grupo:'}


class UploadFileForm(forms.Form):
    file = forms.FileField()


