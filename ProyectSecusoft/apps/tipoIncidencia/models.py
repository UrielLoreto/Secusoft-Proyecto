from django.db import models

# Create your models here.

class TipoIndicencia(models.Model):
    id_tipo = models.AutoField(max_length= 10, primary_key=True)
    tipo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    impacto = models.CharField(max_length= 10)