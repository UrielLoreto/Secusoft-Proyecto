from django import forms
from .models import Persona, Usuario, Alumno, Docente, Padre_Familia

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = (
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'correo',
            'telefono',
            'tipo_persona',
            'sexo'
        )

class RawPersona(forms.Form):
    nombre = forms.CharField()
    apellido = forms.CharField()
    fecha_nacimiento = forms.DateField()
