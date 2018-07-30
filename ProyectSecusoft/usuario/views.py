from django.shortcuts import render
from .models import Persona
from .forms import PersonaForm
# Create your views here.

def index(request):
    return render(request, "usuario/index.html")

def usuario_crear_vista(request):
    form = PersonaForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PersonaForm(request.POST or None)
    context = {
        'form': form
    }
    return render(request, "usuario/nuevo.html", context)


def usuario_mostrar_vista(request):
    obj = Persona.objects.get(id_persona='1')
    context = {
        'nombre': obj.id_persona,
        'fecha de creacion': obj.fecha_creacion,
        'fecha de modificacion': obj.fecha_modificacion ,
        'fecha de nacimiento': obj.fecha_nacimiento,
        'nombre': obj.nombre,
        'apellidos': obj.apellido,
        'email': obj.correo,
        'telefono': obj.telefono,
        'tipo de usuario': obj.tipo_persona,
        'sexo': obj.sexo
    }
    return render(request, "usuario/usuarios.html", context)