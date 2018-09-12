from django import forms
from .models import *


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['token', 'fecha_creacion', 'fecha_modificacion']
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Omar',
            'require': 'true'}),
        label='Nombre(s):')
    apellido = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Gutierrez Martinez',
            'require': 'true'}),
        label='Apellidos(s):')
    fecha_nacimiento = forms.DateInput(attrs={'class': 'form-control'})


class PersonaAlForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['token', 'fecha_creacion', 'fecha_modificacion', 'telefono', 'correo']
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Omar',
            'require': 'true'}),
        label='Nombre(s):')
    apellido = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Gutierrez Martinez',
            'require': 'true'}),
        label='Apellidos(s):')
    fecha_nacimiento = forms.DateInput(attrs={'class': 'form-control'})


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        exclude = ['alumno']
    matricula = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '15110167',
            'require': 'true'}),
        label='Matricula:')


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'require': 'true'}),
        label='Nombre de usuario:')
    contra = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '********',
            'require': 'true',
            'type': 'password'}),
        label='Contraseña:')


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'


class PadreForm(forms.ModelForm):
    class Meta:
        model = PadreFamilia
        fields = '__all__'


class PadreAlumnoForm(forms.ModelForm):
    class Meta:
        model = PadreAlumno
        fields = '__all__'

