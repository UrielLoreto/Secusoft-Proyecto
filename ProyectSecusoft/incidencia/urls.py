from django.urls import path, include
from incidencia.views import *
from rest_framework import routers
router = routers.DefaultRouter()
router.register('tipo_incidencia', TipoIncidenciaView)
app_name = 'incidencias'
urlpatterns = [
    path('', IncidenciaListView.as_view(), name='incidencia-lista'),
    path('importar', import_data, name='incidencia-importar'),
    path('agregar', IncidenciaCreateView.as_view(), name="incidencia-nueva"),
    path('<int:pk>/', IncidenciaDetailView.as_view(), name="incidencia-detalle"),
    path('<int:pk>/modificar/', IncidenciaUpdateView.as_view(), name="incidencia-actualizar"),
    path('<int:pk>/eliminar/', IncidenciaDeleteView.as_view(), name="incidencia-eliminar"),
    path('mobile/api/', include(router.urls))
]
