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
            print("Docente")
            doceente = self.request.user.usuario_id
            queryset = Materia.objects.raw(
                'SELECT materia_materia.*, materia_materiadocente_docente.*, usuario_docente.* '
                'From materia_materia '
                'Inner join materia_materiadocente_docente on materia_materia.id=materia_materiadocente_docente.materiadocente_id '
                'Inner join usuario_docente on materia_materiadocente_docente.docente_id=usuario_docente.id '
                'where usuario_docente.docente_id=%s', [doceente])

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


class MateriaCreateView(CreateView):  # Mostrar todos lo usuarios
    template_name = 'materia/materia_agregar.html'
    form_class = MateriaForm
    segundo_form_class = MateriaDocenteForm

    def get_context_data(self, **kwargs):
        context = super(MateriaCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['alumno'] = True
        context['title'] = 'Agregar Materia'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form_class(request.POST)
        if form.is_valid():
            print("Form valido")
        if form2.is_valid():
            print("form2 valido")
        if form.is_valid() and form2.is_valid():
            print("Formularios validos ")
            materia = form.save(commit=False)
            docente = form2.save(commit=False)
            print(form.cleaned_data)
            print(form2.cleaned_data)
            materia.save()
            docente.save()
            docente.materia.add(materia)
            docente.docente.add(request.POST['docente'])
            docente.save()
            return HttpResponseRedirect('..')
        else:
            print("MAL")
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)