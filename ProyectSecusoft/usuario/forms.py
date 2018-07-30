from django import forms
from .models import Persona, Usuario, Alumno, Docente, Padre_Familia

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = (
            'nombre',
            'apellido',
            'correo',
            'telefono',
            'tipo_persona',
            'sexo'
        )
