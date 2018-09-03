from django.urls import path
from .views import UsuarioDeleteView, UsuarioUpdateView, UsuarioDetailView, PersonaAlumnoCreateView, UsuarioListView

app_name = 'usuarios'
urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario-lista'),
    path('agregar/alumno', PersonaAlumnoCreateView.as_view(), name='usuario-nuevo-alumno'),
    # path('agregar/docente', UsuarioDocenteCreateView.as_view(), name='usuario-nuevo-docente'),
    # path('agregar/padredefamilia', UsuarioPadreCreateView.as_view(), name='usuario-nuevo-padre'),
    path('<int:id>/', UsuarioDetailView.as_view(), name='usuario-detalle'),
    path('<int:id>/modificar/', UsuarioUpdateView.as_view(), name='usuario-actualizar'),
    path('<int:id>/eliminar/', UsuarioDeleteView.as_view(), name='usuario-eliminar'),
]
