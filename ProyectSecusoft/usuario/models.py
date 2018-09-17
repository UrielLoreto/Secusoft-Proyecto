from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
    )
# Create your models here.


class Persona(models.Model):
    persona_tipo = (
        ('1', 'Administrador'),
        ('2', 'Docente'),
        ('3', 'Padre de familia'),
        ('4', 'Alumno'),
    )
    sexo_tipo = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    tipo_persona = models.CharField(max_length=2, choices=persona_tipo, default='4')
    sexo = models.CharField(max_length=1, choices=sexo_tipo, default='H')
    fecha_nacimiento = models.DateField()
    token = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Alumno(models.Model):
    grado_tipo = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),)
    grupo_tipo = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),)
    alumno = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)
    matricula = models.CharField(help_text="Matricula del alumno", max_length=8, primary_key=True, unique=True)
    grado = models.CharField(max_length=10, choices=grado_tipo, default='1')
    grupo = models.CharField(max_length=10, choices=grupo_tipo, default='A')

    def __str__(self):
        return self.matricula


class PadreFam(models.Model):
    padre = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)


class PadreAlumno(models.Model):
    padre = models.ManyToManyField(PadreFam)
    alumno = models.ManyToManyField(Alumno)


class Docente(models.Model):
    tutor_tipo = (
        ('1', 'Si'),
        ('2', 'No'),
        ('3', 'Temporal'),
    )
    docente = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tutor = models.CharField(max_length=5, choices=tutor_tipo, default='1')


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password) # change user password
        user_obj.activo = is_active
        user_obj.save(using=self._db)
        return user_obj


class Usuario(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    usuario = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)
    telefono = models.CharField(max_length=10)
    activo = models.BooleanField(default=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] #['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
