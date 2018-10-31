from django.contrib.auth import authenticate, login
from usuario.models import Usuario
from .models import Aviso
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = Usuario.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                    raise forms.ValidationError("Este usuario esta inactivo")
        else:
            raise forms.ValidationError("Correo no registrado")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Credenciales invalidas")
        login(request, user)
        self.user = user
        return data


class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = '__all__'
    asunto = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'require': 'true'}),
        label='Asunto del aviso:')
