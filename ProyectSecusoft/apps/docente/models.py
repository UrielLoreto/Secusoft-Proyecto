from django.db import models

# Create your models here.
from apps import persona


class Docente(models.Model):
    id_doncente = models.ForeignKey(persona)