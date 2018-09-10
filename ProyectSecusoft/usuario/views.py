import itertools
from datetime import datetime
from django.db import transaction
from django.shortcuts import reverse, get_object_or_404, get_list_or_404, render
from .models import *
from django.http import HttpResponseRedirect
from .forms import *
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)


class UsuarioListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'usuario/usuario_lista.html'
    queryset = Persona.objects.exclude(tipo_persona='4')

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset(),
                   'title': 'Lista de usuarios',
                   'year': datetime.now().year,
                   }
        return render(request, self.template_name, context)


class AlumnoListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'usuario/usuario_lista.html'
    queryset = Alumno.objects.raw('Select usuario_alumno.*, usuario_persona.* '
                                  'from usuario_alumno '
                                  'INNER JOIN usuario_persona ON usuario_alumno.alumno_id=usuario_persona.id')

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset(),
                   'title': 'Lista de alumnos',
                   'year': datetime.now().year,
                   'alumno': 'true',
                   }
        return render(request, self.template_name, context)


class DocenteListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'usuario/usuario_lista.html'
    queryset = Persona.objects.filter(tipo_persona='2')

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset(),
                   'title': 'Lista de docentes',
                   'year': datetime.now().year,
                   }
        return render(request, self.template_name, context)


class PersonaAlumnoCreateView(CreateView):  # Agregar nuevo alumno
    model = Persona
    template_name = 'usuario/usuario_agregar.html'
    form_class = PersonaForm
    segundo_form_class = AlumnoForm

    def get_context_data(self, **kwargs):
        context = super(PersonaAlumnoCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form_class(request.POST)
        if form.is_valid():
            print("Form1 valido")
        if form2.is_valid():
            print("fomr2 valido")
        if form.is_valid() and form2.is_valid():
            print("Valido")
            persona = form.save(commit=False)
            form2.matricula = persona.pk
            persona.save()
            return HttpResponseRedirect('..')
        else:
            print("MAL")
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UsuarioPadreCreateView(CreateView):  # Agregar nuevo padre
    template_name = 'usuario/usuario_agregar.html'
    form_class = PersonaForm
    segundo_form_class = PadreForm
    tercer_form_class = UsuarioForm
    cuarto_form_class = PadreAlumnoForm

    def get_context_data(self, **kwargs):
        context = super(UsuarioPadreCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.tercer_form_class(self.request.GET)
        if 'form4' not in context:
            context['form4'] = self.cuarto_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form_class(request.POST)
        form3 = self.tercer_form_class(request.POST)
        form4 = self.cuarto_form_class(request.POST)
        print(form4.data)
        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            print("Valido")
            persona = form.save()
            persona.save()
            usuario = form2.save(persona)
            alumno = form3.save(persona)
            usuario.save()
            alumno.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3, form4=form4))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UsuarioDocenteCreateView(CreateView):  # Agregar nuevo padre
    template_name = 'usuario/usuario_agregar.html'
    form_class = PersonaForm
    segundo_form_class = DocenteForm
    tercer_form_class = UsuarioForm

    def get_context_data(self, **kwargs):
        context = super(UsuarioDocenteCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.tercer_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form_class(request.POST)
        form3 = self.tercer_form_class(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            print("Valido")
            persona = form.save()
            persona.save()
            usuario = form2.save(persona)
            alumno = form3.save(persona)
            usuario.save()
            alumno.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UsuarioDetailView(DetailView):  # Detalle de un usuario por su id
    template_name = 'usuario/usuario_detalle.html'

    def get_object(self, queryset=None):
        _id = self.kwargs.get("id")
        return get_object_or_404(Persona, id_persona=_id)


class UsuarioUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'usuario/usuario_actualizar.html'
    form_class = PersonaForm

    def get_object(self, queryset=None):
        _id = self.kwargs.get("id")
        return get_object_or_404(Persona, id_persona=_id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UsuarioDeleteView(DeleteView):  # Eliminar un usuario por su id

    template_name = 'usuario/usuario_eliminar.html'

    def get_object(self, queryset=None):
        _id = self.kwargs.get("id")
        return get_object_or_404(Persona, id_persona=_id)

    def get_success_url(self):
        return reverse('usuarios:usuario-lista')
