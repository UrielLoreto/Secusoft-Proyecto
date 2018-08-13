from django.urls import path
from .views import (
    cita_crear_vista,
    cita_lista_vista,
    cita_detalle_vista,
    cita_actualizar_vista,
    cita_eliminar_vista,
)

app_name = 'citas'
urlpatterns = [
    path('', cita_lista_vista, name='cita-lista'),
    path('agregar', cita_crear_vista, name="cita-nuevo"),
    path('<int:id>/', cita_detalle_vista, name="cita-detalle"),
    path('<int:id>/modificar', cita_actualizar_vista, name="cita-actualizar"),
    path('<int:id>/eliminar', cita_eliminar_vista, name="cita-eliminar"),
]