from django.db import models
from usuario.models import Docente, Alumno
from cita.models import Cita
from django.urls import reverse

# Create your models here.


class TipoIndicencia(models.Model):
    tipos_incidencia = (
        ('1', 'Administrativa'),
        ('2', 'Conducta'),
        ('3', 'Labor'),
        ('4', 'Otro'),
    )
    tipo_impacto = (
        ('1', 'Leve'),
        ('2', 'Moderado'),
        ('3', 'Grabe'),
    )
    id_tipo = models.AutoField(max_length=10, primary_key=True)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=200)
    tipo = models.CharField(max_length=2, choices=tipos_incidencia, default='1')
    impacto = models.CharField(max_length=10, choices=tipo_impacto, default='1')

    def __str__(self):
        return self.asunto


class Incidencia(models.Model):
    estatus_tipo = (
        ('1', 'Reportada'),
        ('2', 'En Proceso'),
        ('3', 'Atendida'),
        ('4', 'Otro'),
    )
    id_incidencia = models.AutoField(max_length=20, primary_key=True)
    fecha_incidencia = models.DateTimeField()
    estatus = models.CharField(max_length=2, choices=estatus_tipo, default='1')
    observaciones = models.TextField(null=True, blank=True)
    incidencia = models.ForeignKey(TipoIndicencia, on_delete=models.CASCADE)

    def __str__(self):
        return '%s el %s' % (self.incidencia, self.fecha_incidencia.date())

    def get_absolute_url(self):
        return reverse("incidencias:incidencia-detalle", kwargs={"id": self.id_incidencia})


class IncidenciaAlumno(models.Model):
    incidencia = models.ManyToManyField(Incidencia, blank=True)
    alumno = models.ManyToManyField(Alumno, blank=True)


class IncidenciaDocente(models.Model):
    incidencia = models.ManyToManyField(Incidencia, blank=True)
    docente = models.ManyToManyField(Docente, blank=True)


class IncidenciaPadre(models.Model):
    incidencia = models.ManyToManyField(Incidencia, blank=True)


class IncidenciaCita(models.Model):
    incidencia = models.ManyToManyField(Incidencia, blank=True)
    cita = models.ManyToManyField(Cita, blank=True)


class Comentario(models.Model):
    id_comentario = models.AutoField(max_length=20, primary_key=True)
    comentario = models.CharField(max_length=500, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class ComentarioRel(models.Model):
    comentario = models.ManyToManyField(Comentario, blank=True)
    rel = models.ManyToManyField(Cita, blank=True)
    persona = models.ManyToManyField(Docente, blank=True)