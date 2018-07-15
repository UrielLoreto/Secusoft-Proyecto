from django.db import models

# Create your models here.
from apps import citaEstatus

class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    fecha_cita = models.DateTimeField()
    asunto = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=500)
    id_estatus = models.ForeignKey(citaEstatus)

