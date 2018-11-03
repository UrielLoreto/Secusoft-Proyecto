from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from .models import TipoIndicencia, Incidencia


class TipoIncidenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoIndicencia
        fields = ('url', 'id_tipo', 'asunto', 'descripcion', 'get_tipo_display', 'get_impacto_display')
        extra_kwargs = {
                    'url': {'view_name': 'incidencias:incidenciatipo-detalle'}
                }


class IncidenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Incidencia
        fields = ('url', 'id_incidencia',  'fecha_incidencia', 'estatus', 'observaciones', 'incidencia')
        extra_kwargs = {
            'url': {'view_name': 'incidencias:incidencia-detalle'},
            'incidencia': {'view_name': 'incidencias:incidenciatipo-detalle'}
        }

