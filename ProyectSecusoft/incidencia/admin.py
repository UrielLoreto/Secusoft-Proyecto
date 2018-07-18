from django.contrib import admin
from incidencia.models import Incidencia, TipoIndicencia, EstatusIncidencia
# Register your models here.
admin.site.register(Incidencia)
admin.site.register(TipoIndicencia)
admin.site.register(EstatusIncidencia)