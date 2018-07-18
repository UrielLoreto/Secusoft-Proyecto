from django.contrib import admin
from usuario.models import Persona, Padre_Familia, Alumno, Docente, Padre_Alumno, Usuario
# Register your models here.
admin.site.register(Persona)
admin.site.register(Padre_Familia)
admin.site.register(Padre_Alumno)
admin.site.register(Alumno)
admin.site.register(Docente)
admin.site.register(Usuario)