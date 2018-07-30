"""ProyectSecusoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from usuario.views import usuario_mostrar_vista, index, usuario_crear_vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', index, name="usuario"),
    path('usuarios/mostrar', usuario_mostrar_vista, name="mostrar_usuarios"),
    path('usuarios/nuevo', usuario_crear_vista, name="nuevo_usuario"),
    path('citas/', index, name="cita"),
]
