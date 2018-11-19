from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions

from cita.models import Cita
from dashboard.models import Aviso
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


class CitaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'


class AvisoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aviso
        fields = ('id', 'fecha_creacion', 'asunto', 'descripcion')
