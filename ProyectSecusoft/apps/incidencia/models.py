from django.db import models

# Create your models here.

class EstatusIncidencia(models.Model):
    id_estatus = models.AutoField(primary_key=True)
    estatus = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)

class TipoIndicencia(models.Model):
    id_tipo = models.AutoField(max_length= 10, primary_key=True)
    tipo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    impacto = models.CharField(max_length= 10)

class Incidencia(models.Model):
    id_incidencia = models.AutoField(max_length= 20, primary_key=True)
    fecha_incidencia = models.DateTimeField()
    asunto = models.CharField(max_length=200)
    id_estatus = models.ForeignKey(EstatusIncidencia, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=500)
    id_tipo = models.ForeignKey(TipoIndicencia, on_delete=models.CASCADE)
