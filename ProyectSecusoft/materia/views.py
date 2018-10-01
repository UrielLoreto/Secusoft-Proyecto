from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    FormView,
    UpdateView
)
from .models import *
# Create your views here.


class MateriaListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'materia/materia_lista.html'

    def get_queryset(self):
        if self.request.user.usuario.tipo_persona is '2':
            print("Padre de femilia")
            doceente = self.request.user.usuario_id
            queryset = Materia.objects.raw(
                'SELECT materia_materia.*, materia_materiadocente_docente.*, usuario_docente.* '
                'From materia_materia '
                'Inner join materia_materiadocente_docente on materia_materia.id=materia_materiadocente_docente.materiadocente_id '
                'Inner join usuario_docente on materia_materiadocente_docente.docente_id=usuario_docente.id where usuario_docente.docente_id=%s', [doceente])

        elif self.request.user.usuario.tipo_persona is '1':
            queryset = Materia.objects.raw(
                'SELECT materia_materia.*, materia_materiadocente_docente.*, usuario_docente.* '
                'From materia_materia '
                'Inner join materia_materiadocente_docente on materia_materia.id=materia_materiadocente_docente.materiadocente_id '
                'Inner join usuario_docente on materia_materiadocente_docente.docente_id=usuario_docente.id')
        return queryset

    def get(self, request, *args, **kwargs):
        context = {
            'object_list': self.get_queryset(),
            'title': 'Lista de materias',
            'year': datetime.now().year,
        }
        return render(request, self.template_name, context)
