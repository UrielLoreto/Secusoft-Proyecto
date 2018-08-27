from django import forms
from .models import Persona, Usuario, Alumno, Docente, PadreFamilia


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['token']
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Omar'}),
        label='Nombre(s):')
    apellido = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Gutierrez Martinez'}),
        label='Apellidos(s):')
    fecha_nacimiento = forms.DateTimeField(label='Fecha de nacimiento:')
    correo = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@mail.com'}),
        label='Email:')
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '333456260'}),
        label='Telefono:')


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = (
            'nombre',
            'contra',
        )
        labels = {
            'nomre': 'Nombre de usuario',
            'contra': 'Contraseña',
        }


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
