from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from .models import TipoIndicencia


class TipoIncidenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TipoIndicencia
        fields = ('id_tipo', 'asunto', 'descripcion', 'get_tipo_display', 'get_impacto_display')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data