from audioop import reverse

from django.db import models
from usuario.models import Docente
# Create your models here.


class Materia(models.Model):
    grado_tipo = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),)
    grupo_tipo = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),)
    nombre = models.CharField(max_length=50)
    grado = models.CharField(max_length=10, choices=grado_tipo, null=True, blank=True)
    grupo = models.CharField(max_length=10, choices=grupo_tipo, null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.nombre, self.get_grado_display())


class MateriaDocente(models.Model):
    materia = models.ManyToManyField(Materia)
    docente = models.ManyToManyField(Docente)
