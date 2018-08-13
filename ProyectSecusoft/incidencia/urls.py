from django.urls import path
from incidencia.views import IncidenciaUpdateView, IncidenciaDeleteView, IncidenciaDetailView, IncidenciaCreateView, IncidenciaListView

app_name = 'incidencias'
urlpatterns = [
    path('', IncidenciaListView.as_view(), name='incidencia-lista'),
    path('agregar', IncidenciaCreateView.as_view(), name="incidencia-nuevo"),
    path('<int:id>/', IncidenciaDetailView.as_view(), name="incidencia-detalle"),
    path('<int:id>/modificar/', IncidenciaUpdateView.as_view(), name="incidencia-actualizar"),
    path('<int:id>/eliminar/', IncidenciaDeleteView.as_view(), name="incidencia-eliminar"),
]
