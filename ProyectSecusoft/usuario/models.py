from django.db import models
from django.urls import reverse

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
    id_persona = models.AutoField(primary_key=True, editable=False, help_text="ID unico de cada persona")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_nacimiento = models.DateField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    tipo_persona = models.CharField(max_length=2, choices=persona_tipo, default='4')
    sexo = models.CharField(max_length=1, choices=sexo_tipo, default='H')
    token = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("usuarios:usuario-detalle", kwargs={"id": self.id_persona})


class Usuario(models.Model):
    usuario = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20, unique=True)
    contra = models.CharField(max_length=30)


class PadreFamilia(models.Model):
    padre = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)


class Alumno(models.Model):
    grado_tipo = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),)
    grupo_tipo = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),)
    alumno = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    matricula = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=10, choices=grado_tipo, default='1')
    grupo = models.CharField(max_length=10, choices=grupo_tipo, default='A')


class PadreAlumno(models.Model):
    padre = models.ManyToManyField(PadreFamilia)
    alumno = models.ManyToManyField(Alumno)


class Docente(models.Model):
    tutor_tipo = (
        ('1', 'Si'),
        ('2', 'No'),
        ('3', 'Temporal'),
    )
    docente = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    tutor = models.CharField(max_length=5, choices=tutor_tipo, default='1')
