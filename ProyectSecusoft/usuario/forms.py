from django import forms
from .models import *
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminDateWidget

User = get_user_model()


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['token', 'fecha_creacion', 'fecha_modificacion', 'tipo_persona']
        labels = {'fecha_nacimiento': 'Fecha de nacimiento:',
                  'sexo': 'Sexo:'}
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
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-group',
            'autocomplete': 'off',
            'require': 'true'}),
        label='Fecha de nacimiento:')


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


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ('tutor',)


class PadreForm(forms.ModelForm):
    class Meta:
        model = PadreFam
        fields = '__all__'
        exclude = ('padre',)


class PadreAlumnoForm(forms.ModelForm):
    class Meta:
        model = PadreAlumno
        fields = '__all__'
        exclude = ('padre',)
        labels = {'alumno': 'Hijo(s):'}


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Contraseña:', widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'require': 'true'})
                )
    password2 = forms.CharField(label='Confirmacion de Contraseña:', widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'require': 'true'})
                )

    class Meta:
        model = Usuario
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        usuario = super(RegisterForm, self).save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        # obj = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()
        if commit:
            usuario.save()
        return usuario


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'active', 'admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


