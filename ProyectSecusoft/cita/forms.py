from django import forms
from .models import *

#
# class PersonaForm(forms.ModelForm):
#     class Meta:
#         model = Persona
#         fields = (
#             'nombre',
#             'apellido',
#             'fecha_nacimiento',
#             'correo',
#             'telefono',
#             'tipo_persona',
#             'sexo'
#         )


class RawCita(forms.Form):
    nombre = forms.CharField()
    apellido = forms.CharField()
    fecha_nacimiento = forms.DateField()
