from django.shortcuts import reverse, get_object_or_404, get_list_or_404, render
from .models import Incidencia, IncidenciaAlumno
from .forms import IncidenciaForm
from usuario.forms import PersonaForm
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

#
# # class IncidenciaListView(ListView):  # Mostrar todos lo incidencias
#     template_name = 'incidencia/incidencia_lista.html'
#     # queryset = get_list_or_404(Incidencia)
#
#     def get_queryset(self):
#         return self.queryset
#
#     def get(self, request, *args, **kwargs):
#         context = {'object_list': self.get_queryset()}
#         return render(request, self.template_name, context)


class IncidenciaCreateView(CreateView):  # Agregar nuevo incidencia
    model = Incidencia
    template_name = 'incidencia/incidencia_agregar.html'
    form_class = IncidenciaForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


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
