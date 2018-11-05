from django.urls import path, include
from django.views.generic import RedirectView
from incidencia.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tipo_incidencia', TipoIncidenciaView)
router.register('incidencia', IncidenciaView)
router.register('cita', CitaView)

app_name = 'incidencias'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard:index')),
    path('lista', IncidenciaListView.as_view(), name='incidencia-lista'),
    path('lista/<int:grado>/<str:grupo>', IncidenciaAlListView.as_view(), name='incidencia-lista-al'),
    path('importar', import_data, name='incidencia-importar'),
    path('agregar/<int:grado>/<str:grupo>', IncidenciaCreateView.as_view(), name="incidencia-nueva"),
    path('agregar/alumnos/<int:pk>/<int:grado>/<str:grupo>', IncidenciaAlCreateView.as_view(), name="incidencia-nueva-al"),
    path('<int:pk>/', IncidenciaDetailView.as_view(), name="incidencia-detalle"),
    path('agregar/tipo', IncidenciaTipoCreateView.as_view(), name="incidenciatipo-nueva"),
    path('tipo/<int:pk>/', IncidenciaTipoDetailView.as_view(), name="incidenciatipo-detalle"),
    path('tipo/lista', IncidenciatipoListView.as_view(), name='incidenciatipo-lista'),
    path('<int:pk>/modificar/', IncidenciaUpdateView.as_view(), name="incidencia-actualizar"),
    path('<int:pk>/eliminar/', IncidenciaDeleteView.as_view(), name="incidencia-eliminar"),
    path('mobile/api/', include(router.urls)),
    path('mobile/api/api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
]
