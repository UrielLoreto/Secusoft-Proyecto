from django.db import models
from django.urls import reverse

# Create your models here.


class Alumno(models.Model):
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
    sexo_tipo = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=sexo_tipo, default='H')
    fecha_nacimiento = models.DateField()
    matricula = models.CharField(help_text="Matricula del alumno", max_length=8, primary_key=True, unique=True)
    grado = models.CharField(max_length=10, choices=grado_tipo, default='1')
    grupo = models.CharField(max_length=10, choices=grupo_tipo, default='A')

    def __str__(self):
        return 'Grado: %s,  %s %s %s' % (self.get_grado_display(), self.nombre, self.apellido, self.matricula)

    def get_absolute_url(self):
        return reverse('alumnos:alumnos-detalle', kwargs={'pk': self.matricula})

