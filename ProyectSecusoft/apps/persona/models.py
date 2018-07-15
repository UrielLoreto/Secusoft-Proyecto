from django.db import models

# Create your models here.

class Persona(models.Model):
    id_persona= models.AutoField(max_length= 10, primary_key=True)
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