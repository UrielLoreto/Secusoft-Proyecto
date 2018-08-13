from django.contrib import admin
from incidencia.models import *
# Register your models here.
admin.site.register(Incidencia)
admin.site.register(TipoIndicencia)
admin.site.register(Comentario)
admin.site.register(ComentarioRel)
admin.site.register(IncidenciaAlumno)
admin.site.register(IncidenciaCita)
admin.site.register(IncidenciaDocente)
admin.site.register(IncidenciaPadre)
