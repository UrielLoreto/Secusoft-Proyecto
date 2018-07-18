import uuid

from django.db import models

# Create your models here.

class Persona(models.Model):
    id_persona = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_nacimiento = models.DateField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=10)
    tipo_persona = models.CharField(max_length=2)
    sexo = models.CharField(max_length=10)
    token = models.CharField(max_length=80)

class Usuario(models.Model):
    usuario = models.ForeignKey(Persona, on_delete=models.CASCADE)
    nombre = models.CharField(max_length= 20, unique=True)
    contra = models.CharField(max_length= 30)
    nivel = models.CharField(max_length=2)

class Padre_Familia(models.Model):
    padre = models.ForeignKey(Persona, on_delete=models.CASCADE)

class Alumno(models.Model):
    alumno = models.ForeignKey(Persona, on_delete=models.CASCADE)
    matricula = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=5)
    grupo = models.CharField(max_length=5)

class Padre_Alumno(models.Model):
    padre = models.ForeignKey(Padre_Familia, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

class Docente(models.Model):
    doncente = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tutor = models.CharField(max_length=5)