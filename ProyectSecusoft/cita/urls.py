from django.urls import path
from django.views.generic import RedirectView

from .views import *
app_name = 'citas'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard:index')),
    path('incidencia', CitaIncidenciaListView.as_view(), name='cita-incidencia-lista'),
    path('incidencia/lista/<int:grado>/<str:grupo>', CitaIncidenciaAlListView.as_view(), name='cita-incidencia-lista-al'),
    path('incidencia/agregar/<int:grado>/<str:grupo>', CitaIncidenciaAlCreateView.as_view(), name="cita-incidencia-nueva-al"),
    path('incidencia/cita/<int:pk>/<int:grado>/<str:grupo>', IncidenciaAlCreateView.as_view(), name="cita-incidencia-nueva-al-cit"),
    path('incidencia/agregar', CitaIncidenciaCreateView.as_view(), name="cita-incidencia-nueva"),
    path('incidencia/<int:pk>/modificar', CitaIncidenciaUpdateView.as_view(), name="cita-incidencia-actualizar"),
    path('incidencia/<int:pk>/', CitaIncidenciaDetailView.as_view(), name="cita-incidencia-detalle"),
]