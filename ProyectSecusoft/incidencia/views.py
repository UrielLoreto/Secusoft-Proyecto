from django.shortcuts import reverse, get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect
from .forms import *
from usuario.forms import PersonaForm
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)


class IncidenciaCreateView(CreateView):  # Agregar nuevo incidencia
    template_name = 'incidencia/incidencia_agregar.html'
    form_class = IncidenciaForm
    segundo_form_class = IncidenciaAlForm
    tercer_form_class = IncidenciaTipoForm

    def get_context_data(self, **kwargs):
        context = super(IncidenciaCreateView, self).get_context_data(**kwargs)
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
            incidencia = form.save(commit=False)
            incidencia.alumno = form2.save(incidencia)
            incidencia.docente = form3.save(incidencia)
            incidencia.save()
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))


class IncidenciaDetailView(DetailView):  # Detalle de un incidencia por su id
    model = Incidencia
    template_name = 'incidencia/incidencia_detalle.html'

    def get_object(self, queryset=None):
        _id = self.kwargs.get("id")
        return get_object_or_404(Incidencia, id_incidencia=_id)


class IncidenciaUpdateView(UpdateView):  # Mofificar un incidencia por su id
    model = Incidencia
    template_name = 'incidencia/incidencia_actualizar.html'
    form_class = IncidenciaForm

    def get_object(self, queryset=None):
        _id = self.kwargs.get("id")
        return get_object_or_404(Incidencia, id_incidencia=_id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class IncidenciaDeleteView(DeleteView):  # Eliminar un incidencia por su id
    model = Incidencia
    template_name = 'incidencia/incidencia_eliminar.html'

    def get_object(self, queryset=None):
        _id = self.kwargs.get("id")
        return get_object_or_404(Incidencia, id_incidencia=_id)

    def get_success_url(self):
        return reverse('incidencias:incidencia-lista')


class IncidenciaListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'incidencia/incidencia_lista.html'
    queryset = Alumno.objects.raw('Select incidencia_incidencia.*, incidencia_incidenciaalumno_alumno.* '
                                  'from incidencia_incidencia '
                                  'INNER JOIN incidencia_incidenciaalumno_alumno ON indicencia_incidencia.id_incidencia=incidencia_incidenciaalumno_alumno.alumno_id')

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