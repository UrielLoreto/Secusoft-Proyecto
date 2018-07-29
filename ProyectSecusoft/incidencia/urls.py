from django.urls import path
from incidencia.views import index


urlpatterns = [
    path('', index),
]
