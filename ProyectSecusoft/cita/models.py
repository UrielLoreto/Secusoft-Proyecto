from django.db import models

# Create your models here.

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