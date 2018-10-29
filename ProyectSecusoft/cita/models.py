from django.db import models
from incidencia.models import Incidencia
# Create your models here.
from usuario.models import Docente


class Cita(models.Model):
    estatus_tipo = (
        ('1', 'Solicitada'),
        ('2', 'Aceptada'),
        ('3', 'Atendida'),
    )
    id_cita = models.AutoField(max_length=20, primary_key=True)
    fecha_cita = models.DateTimeField()
    asunto = models.CharField(max_length=200)
    observaciones = models.TextField()
    estatus = models.CharField(max_length=2, choices=estatus_tipo, default='1')
    descripcion = models.TextField()


class CitaIncidencia(models.Model):
    incidencia = models.ManyToManyField(Incidencia)
    cita = models.ManyToManyField(Cita)


class Comentario(models.Model):
    id_comentario = models.AutoField(max_length=20, primary_key=True)
    comentario = models.CharField(max_length=500, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class ComentarioRel(models.Model):
    comentario = models.ManyToManyField(Comentario, blank=True)
    rel = models.ManyToManyField(Cita, blank=True)
    persona = models.ManyToManyField(Docente, blank=True)



