from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *
from .forms import RawCita
# Create your views here.


def cita_lista_vista(request):  # Mostrar todos lo citas
    obj = Cita.objects.all()
    context = {
        "lista_objetos": obj
    }
    return render(request, "cita/cita_lista.html", context)


def cita_crear_vista(request):  # Agregar nuevo cita
    my_form = RawCita()
    if request.method == "POST":
        my_form = RawCita(request.POST)
        if my_form.is_valid():
            print(my_form.cleaned_data)
        else:
            print(my_form.errors)
    context = {
        "form": my_form
    }
    return render(request, "cita/cita_agregar.html", context)


def cita_detalle_vista(request, id):  # Detalle de un cita por su id
    obj = get_object_or_404(Cita, id_cita=id)
    context = {
        "persona": obj
    }
    return render(request, "cita/cita_detalle.html", context)


def cita_actualizar_vista(request, id):  # Mofificar un cita por su id
    obj = get_object_or_404(Cita, id_cita=id)
    context = {
        "persona": obj
    }
    return render(request, "cita/incidencia_actualizar.html", context)


def cita_eliminar_vista(request, id):  # Eliminar un cita por su id
    obj = get_object_or_404(Cita, id_cita=id)
    context = {
        "persona": obj
    }
    return render(request, "cita/cita_eliminar.html", context)
