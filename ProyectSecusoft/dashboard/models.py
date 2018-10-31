from django.db import models
from django.urls import reverse

# Create your models here.


class Aviso(models.Model):
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
    usuario_tipo = (
        ('1', 'Todos'),
        ('2', 'Docentes'),
        ('3', 'Padres de familia'),
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asunto = models.CharField(max_length=50)
    descripcion = models.TextField()
    dirigido_a = models.CharField(max_length=2, choices=usuario_tipo, null=False, blank=False)
    grupo = models.CharField(max_length=10, choices=grupo_tipo, null=True, blank=True)
    grado = models.CharField(max_length=10, choices=grado_tipo, null=True, blank=True)

    def __str__(self):
        return '%s el %s' % (self.asunto, self.fecha_creacion)

    def get_absolute_url(self):
        return reverse('dashboard:aviso-detalle', kwargs={'pk': self.id})