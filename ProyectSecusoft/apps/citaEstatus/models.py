from django.db import models

# Create your models here.

class CitaEstatus(models.Model):
    id_estatus = models.AutoField(primary_key=True)
    estatus = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)