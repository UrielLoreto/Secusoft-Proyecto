from rest_framework import serializers
from .models import TipoIndicencia


class TipoIncidenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoIndicencia
        fields = ('id_tipo', 'asunto', 'descripcion', 'get_tipo_display', 'get_impacto_display')
