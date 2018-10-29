from django.urls import path
from django.views.generic import RedirectView

from .views import *
app_name = 'citas'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard:index')),
    path('incidencia', CitaIncidenciaListView.as_view(), name='cita-incidencia-lista'),
    path('incidencia/agregar', CitaIncidenciaCreateView.as_view(), name="cita-incidencia-nueva"),
    path('incidencia/modificar', CitaIncidenciaUpdateView.as_view(), name="cita-incidencia-actualizar"),
    path('incidencia/<int:pk>/', CitaIncidenciaDetailView.as_view(), name="cita-incidencia-detalle"),
]