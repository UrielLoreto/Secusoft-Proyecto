from django.db import models

# Create your models here.
from apps import persona


class Usuario(models.Model):
    id_persona = models.ForeignKey(persona)
    usuario = models.CharField(max_length= 20, unique= True)
    contra = models.CharField(max_length= 30)
    nivel = models.CharField(max_length=2)