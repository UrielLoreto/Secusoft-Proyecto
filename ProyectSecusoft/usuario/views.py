from django.db import transaction
from django.shortcuts import reverse, get_object_or_404, get_list_or_404, render
from .models import Persona
from django.http import HttpResponseRedirect
from .forms import PersonaForm, UsuarioForm, AlumnoForm, DocenteForm
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)


class UsuarioListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'usuario/usuario_lista.html'
    queryset = get_list_or_404(Persona)

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset()}
        return render(request, self.template_name, context)


class UsuarioAlumnoCreateView(CreateView):  # Agregar nuevo usuario
    template_name = 'usuario/usuario_agregar.html'
    form_class = PersonaForm
    segundo_form_class = UsuarioForm
    tercer_form_class = AlumnoForm

    def get_context_data(self, **kwargs):
        context = super(UsuarioAlumnoCreateView, self).get_context_data(**kwargs)
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
