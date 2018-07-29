from django.urls import path
from usuario.views import index


urlpatterns = [
    path('', index),
]
