from django.urls import path
from .views import *
app_name = 'usuarios'
urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario-lista'),
    path('alumnos', AlumnoListView.as_view(), name='usuario-lista-alumnos'),
    path('alumnos/<int:pk>/', AlumnoDetailView.as_view(), name='usuario-detalle-alumnos'),
    path('alumnos/<int:pk>/modificar/', AlumnoUpdateView.as_view(), name='usuario-actualizar-alumnos'),
    path('padres', PadreListView.as_view(), name='usuario-lista-padre'),
    path('docentes', DocenteListView.as_view(), name='usuario-lista-docentes'),
    path('agregar/alumno', PersonaAlumnoCreateView.as_view(), name='usuario-nuevo-alumno'),
    path('agregar/docente', UsuarioDocenteCreateView.as_view(), name='usuario-nuevo-docente'),
    path('agregar/padredefamilia', UsuarioPadreCreateView.as_view(), name='usuario-nuevo-padre'),
    path('<int:pk>/', UsuarioDetailView.as_view(), name='usuario-detalle'),
    path('<int:pk>/modificar/', UsuarioUpdateView.as_view(), name='usuario-actualizar'),
    path('<int:id>/eliminar/', UsuarioDeleteView.as_view(), name='usuario-eliminar'),
]
