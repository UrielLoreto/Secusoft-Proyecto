from django.db import models

# Create your models here.
from apps import persona


class Alumno(models.Model):
    id_alumno = models.ForeignKey(persona)
    matricula = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=5)
    grupo = models.CharField(max_length=5)
