from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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
        if self.request.user.tipo_persona is '2':
            doceente = self.request.user.id
            queryset = Materia.objects.raw(
                'SELECT DISTINCT materia_materia.* FROM usuario_docente '
                'INNER JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
                'INNER JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
                'INNER JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
                'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
                'WHERE usuario_usuario.id = %s ORDER by materia_materia.grado', [doceente])
            return queryset

        elif self.request.user.tipo_persona is '1':
            queryset = Materia.objects.raw(
                    'SELECT DISTINCT materia_materia.*, usuario_docente.*, usuario_usuario.nombre as nombre2, usuario_usuario.apellido as apellido2 FROM usuario_docente '
                    'INNER JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
                    'INNER JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
                    'INNER JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
                    'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
                    'ORDER by materia_materia.id')
            return queryset

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            id = self.request.user.id
            materias = Materia.objects.raw(
                'SELECT DISTINCT materia_materia.* FROM usuario_docente '
                'INNER JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
                'INNER JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
                'INNER JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
                'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
                'WHERE usuario_usuario.id = %s ORDER by materia_materia.grado', [id])
            context = {
                'object_list': self.get_queryset(),
                'materias': materias,
                'title': 'Lista de materias',
                'year': datetime.now().year,
            }
            return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse('dashboard:index'))


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


class MateriaDetailView(DetailView):  # Detalle de un alumno por su id
    template_name = 'materia/materia_detalle.html'
    model = Materia

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(MateriaDetailView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = Materia.objects.filter(id=_id)
        queryset2 = Materia.objects.raw(
            'SELECT materia_materia.id as khe ,materia_materia.*, usuario_docente.*, usuario_usuario.id as idd, usuario_usuario.nombre as nombre2, usuario_usuario.apellido as apellido2 FROM usuario_docente '
            'INNER JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
            'INNER JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
            'INNER JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
            'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
            'WHERE materia_materia.id = %s ORDER by materia_materia.id', [_id])
        context["object"] = queryset
        context["padre"] = queryset2
        context['year'] = datetime.now().year
        context['Alumno'] = True
        context['title'] = 'Detalles de la materia'
        return context


class MateriaUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'materia/materia_actualizar.html'
    model = Materia
    form_class = MateriaForm

    def get_context_data(self, **kwargs):
        context = super(MateriaUpdateView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = Materia.objects.filter(id=_id)
        print(queryset)
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['title'] = 'Actualizar materia'
        return context


class MateriaDocenteUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'materia/materia_actualizar.html'
    model = MateriaDocente
    form_class = MateriaDocenteForm

    def get_context_data(self, **kwargs):
        context = super(MateriaDocenteUpdateView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = MateriaDocente.objects.filter(id=_id)
        print(queryset)
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['title'] = 'Actualizar materia-docente'
        return context

    def get_success_url(self):
        return HttpResponseRedirect(reverse('materias:materia-lista'))