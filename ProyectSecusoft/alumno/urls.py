from django.urls import path
from django.views.generic import RedirectView

from .views import *
app_name = 'alumnos'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard:index')),
    path('lista', AlumnoListView.as_view(), name='alumnos-lista'),
    path('descargas', AlumnoDownloadView.as_view(), name='alumnos-descargas'),
    path('importar', import_data, name='alumnos-importar'),
    path('<int:pk>/', AlumnoDetailView.as_view(), name='alumnos-detalle'),
    path('<int:pk>/modificar/', AlumnoUpdateView.as_view(), name='alumnos-actualizar'),
    path('agregar', AlumnoCreateView.as_view(), name='alumnos-nuevo'),
]
