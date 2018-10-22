from django.urls import path
from .views import *
app_name = 'usuarios'
urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario-lista'),
    path('perfil/', PerilUsuario, name='usuario-perfil'),
    path('perfil/change-password', change_password, name='change-password'),
    path('perfil/modificar', PerilUsuarioUpdate.as_view(), name='usuario-perfil-actualizar'),
    path('padres', PadreListView.as_view(), name='usuario-lista-padre'),
    path('padres/<int:pk>/alumnos', PadreAlumnoUpdateView.as_view(), name='usuario-alumno-padre'),
    path('docentes', DocenteListView.as_view(), name='usuario-lista-docentes'),
    path('docentes/<int:pk>/modificar/', UsuarioDocenteUpdateView.as_view(), name='usuario-actualizar'),
    path('agregar/docente', UsuarioDocenteCreateView.as_view(), name='usuario-nuevo-docente'),
    path('agregar/padredefamilia', UsuarioPadreCreateView.as_view(), name='usuario-nuevo-padre'),
    path('<int:pk>/', UsuarioDetailView.as_view(), name='usuario-detalle'),
    path('<int:pk>/modificar/', UsuarioPadreUpdateView.as_view(), name='usuario-padre-actualizar'),
    path('<int:id>/eliminar/', UsuarioDeleteView.as_view(), name='usuario-eliminar'),
]
