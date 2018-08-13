from django import forms
from .models import Persona, Usuario, Alumno, Docente, PadreFamilia


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
            'sexo',
        )


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = (
            'nombre',
            'contra',
        )


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = (
            'matricula',
            'grado',
            'grupo',
        )


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = (
            'tutor',
        )
