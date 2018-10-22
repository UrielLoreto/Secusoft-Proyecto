from django.urls import path
from .views import *
app_name = 'alumnos'
urlpatterns = [
    path('', AlumnoListView.as_view(), name='alumnos-lista'),
    path('importar', import_data, name='alumnos-importar'),
    path('<int:pk>/', AlumnoDetailView.as_view(), name='alumnos-detalle'),
    path('<int:pk>/modificar/', AlumnoUpdateView.as_view(), name='alumnos-actualizar'),
    path('agregar', AlumnoCreateView.as_view(), name='alumnos-nuevo'),
]
