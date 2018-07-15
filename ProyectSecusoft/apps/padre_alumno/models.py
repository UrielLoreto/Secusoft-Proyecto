from django.db import models

# Create your models here.
from apps import padre_familia, alumno


class Padre_Alumno(models.Model):
    id_padre = models.ForeignKey(padre_familia)
    id_alumno = models.ForeignKey(alumno)