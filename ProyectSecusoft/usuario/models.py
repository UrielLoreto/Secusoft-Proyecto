import uuid

from django.db import models

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
    id_persona = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="ID unico de cada persona")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_nacimiento = models.DateField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=10)
    tipo_persona = models.CharField(max_length=2, choices=persona_tipo, default='4')
    sexo = models.CharField(max_length=10, choices=sexo_tipo, default='H')
    token = models.CharField(max_length=80, null=True, blank=True)

class Usuario(models.Model):
    usuario = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length= 20, unique=True)
    contra = models.CharField(max_length= 30)
    nivel = models.CharField(max_length=2)

class Padre_Familia(models.Model):
    padre = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)

class Alumno(models.Model):
    alumno = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    matricula = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=5)
    grupo = models.CharField(max_length=5)

class Padre_Alumno(models.Model):
    padre = models.ManyToManyField(Padre_Familia)
    alumno = models.ManyToManyField(Alumno)

class Docente(models.Model):
    tutor_tipo = (
        ('1', 'Si'),
        ('2', 'No'),
        ('3', 'Temporal'),
    )
    doncente = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    tutor = models.CharField(max_length=5, choices=tutor_tipo, default='2')