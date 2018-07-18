from django.db import models

# Create your models here.

class CitaEstatus(models.Model):
    id_estatus = models.AutoField(primary_key=True)
    estatus = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

class Cita(models.Model):
    id_cita = models.AutoField(max_length= 20, primary_key=True)
    fecha_cita = models.DateTimeField()
    asunto = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=500)
    estatus = models.ForeignKey(CitaEstatus, on_delete=models.CASCADE)
