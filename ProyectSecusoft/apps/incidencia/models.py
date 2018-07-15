from django.db import models

# Create your models here.
from apps import tipoIncidencia, estatusIncidencia


class Incidencia(models.Model):
    id_incidencia = models.AutoField(primary_key=True)
    fecha_incidencia = models.DateTimeField()
    asunto = models.CharField(max_length=200)
    id_estatus = models.ForeignKey(estatusIncidencia)
    observaciones = models.CharField(max_length=500)
    id_tipo = models.ForeignKey(tipoIncidencia)
