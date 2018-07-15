from django.db import models

# Create your models here.
from apps import persona


class Padre_Familia(models.Model):
    id_padre = models.ForeignKey(persona)
