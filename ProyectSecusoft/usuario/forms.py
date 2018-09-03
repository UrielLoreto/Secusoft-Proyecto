from django import forms
from .models import Persona, Usuario, Alumno, Docente, PadreFamilia

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['token', 'fecha_creacion', 'fecha_modificacion', 'correo', 'telefono']
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
    tipo_persona = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'true',
            'value': '4'}))
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


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'
