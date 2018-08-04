from django.shortcuts import render
from .models import Persona
from .forms import PersonaForm, RawPersona
# Create your views here.

def index(request):
    return render(request, "usuario/index.html")

def usuario_crear_vista(request):
    my_form = RawPersona()
    if request.method == "POST":
        my_form = RawPersona(request.POST)
        if my_form.is_valid():
            print(my_form.cleaned_data)
        else:
            print(my_form.errors)
    context = {
        "form": my_form
    }
    return render(request, "usuario/nuevo.html", context)


# def usuario_crear_vista(request):
#     form = PersonaForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = PersonaForm()
#     context = {
#         'form': form
#     }
#     return render(request, "usuario/nuevo.html", context)

#
def usuario_mostrar_vista(request):
    obj = Persona.objects.all()
    context = {
        "lista_objetos": obj
    }
    return render(request, "usuario/usuarios.html", context)

