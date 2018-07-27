from django.db import models
from usuario.models import Docente, Padre_Familia, Alumno
from cita.models import Cita

# Create your models here.

class TipoIndicencia(models.Model):
    id_tipo = models.AutoField(max_length= 10, primary_key=True)
    tipo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    impacto = models.CharField(max_length= 10)


class Incidencia(models.Model):
    estatus_tipo = (
        ('1', 'Reportada'),
        ('2', 'En Proceso'),
        ('3', 'Atendida'),
        ('4', 'Otro'),
    )
    id_incidencia = models.AutoField(max_length=20, primary_key=True)
    fecha_incidencia = models.DateTimeField()
    asunto = models.CharField(max_length=200)
    estatus = models.CharField(max_length=2, choices=estatus_tipo, default='1')
    observaciones = models.CharField(max_length=500)
    tipo = models.ForeignKey(TipoIndicencia, null=True, blank=True, on_delete=models.CASCADE)


class Incidencia_docente(models.Model):
    incidencia = models.ManyToManyField(Incidencia)
    docente = models.ManyToManyField(Docente)


class Incidencia_padre(models.Model):
    incidencia = models.ManyToManyField(Incidencia)
    padre = models.ManyToManyField(Padre_Familia)


class Incidencia_alumno(models.Model):
    incidencia = models.ManyToManyField(Incidencia)
    alumno = models.ManyToManyField(Alumno)


class Incidencia_cita(models.Model):
    incidencia = models.ManyToManyField(Incidencia)
    cita = models.ManyToManyField(Cita)


class Comentario(models.Model):
    id_comentario = models.AutoField(max_length=20, primary_key=True)
    comentario = models.CharField(max_length=500, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Comentario_rel(models.Model):
    comentario = models.ManyToManyField(Comentario)
    rel = models.ManyToManyField(Cita)
    persona = models.ManyToManyField(Docente)