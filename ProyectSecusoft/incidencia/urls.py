from django.urls import path, include
from django.views.generic import RedirectView

from incidencia.views import *
from rest_framework import routers
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('tipo_incidencia', TipoIncidenciaView)


app_name = 'incidencias'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard:index')),
    path('lista', IncidenciaListView.as_view(), name='incidencia-lista'),
    path('importar', import_data, name='incidencia-importar'),
    path('agregar', IncidenciaCreateView.as_view(), name="incidencia-nueva"),
    path('<int:pk>/', IncidenciaDetailView.as_view(), name="incidencia-detalle"),
    path('<int:pk>/modificar/', IncidenciaUpdateView.as_view(), name="incidencia-actualizar"),
    path('<int:pk>/eliminar/', IncidenciaDeleteView.as_view(), name="incidencia-eliminar"),
    path('mobile/api/', include(router.urls)),
    path('mobile/api/api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
]
