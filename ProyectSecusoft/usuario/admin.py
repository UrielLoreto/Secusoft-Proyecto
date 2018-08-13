from django.contrib import admin
from usuario.models import Persona, PadreFamilia, Alumno, Docente, PadreAlumno, Usuario
# Register your models here.
admin.site.register(Persona)
admin.site.register(PadreFamilia)
admin.site.register(PadreAlumno)
admin.site.register(Alumno)
admin.site.register(Docente)
admin.site.register(Usuario)