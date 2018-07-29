from django.conf.urls import url
from cita.views import index


urlpatterns = [
    url('', index),
]
