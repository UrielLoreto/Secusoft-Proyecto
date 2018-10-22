from datetime import datetime
from django.shortcuts import redirect, get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import *
from django.contrib import messages
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

    def get_context_data(self, **kwargs):
        context = super(IncidenciaCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['title'] = 'Agregar incidencia'
        context['incidencias'] = TipoIndicencia.objects.all()
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
            persona = form.save(commit=False)
            docente = form2.save(commit=False)
            print(form.cleaned_data)
            print(form2.cleaned_data)
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

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


class IncidenciaListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'incidencia/incidencia_lista.html'

    def get_queryset(self):
        if self.request.user.tipo_persona is '3':
            padreid = self.request.user.usuario_id
            queryset = Incidencia.objects.raw('Select alumno_alumno.*, usuario_padrealumno_alumno.padrealumno_id, usuario_padrealumno_padre.padrefam_id, usuario_padrefam.padre_id, incidencia_incidencia.*,incidencia_tipoindicencia.* '
                                              'FROM usuario_alumno '
                                              'INNER JOIN usuario_persona ON alumno_alumno.alumno_id=usuario_persona.id  '
                                              'INNER JOIN usuario_padrealumno_alumno ON usuario_alumno.matricula=usuario_padrealumno_alumno.alumno_id '
                                              'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_alumno.padrealumno_id=usuario_padrealumno_padre.padrealumno_id '
                                              'INNER JOIN usuario_padrefam ON usuario_padrealumno_padre.padrefam_id=usuario_padrefam.id '
                                              'INNER JOIN incidencia_incidenciaalumno_alumno  ON usuario_alumno.matricula=incidencia_incidenciaalumno_alumno.alumno_id '
                                              'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_alumno.incidenciaalumno_id  '
                                              'INNER JOIN incidencia_tipoindicencia on incidencia_tipoindicencia.id_tipo=incidencia_incidencia.incidencia_id '
                                              'WHERE usuario_padrefam.padre_id=%s', [padreid])
        else:
            queryset = Incidencia.objects.raw('Select alumno_alumno.*, usuario_padrealumno_alumno.padrealumno_id, usuario_padrealumno_padre.padrefam_id, usuario_padrefam.padre_id, incidencia_incidencia.*,incidencia_tipoindicencia.* '
                                              'FROM alumno_alumno '
                                              'INNER JOIN usuario_persona ON alumno_alumno.alumno_id=usuario_persona.id  '
                                              'INNER JOIN usuario_padrealumno_alumno ON usuario_alumno.matricula=usuario_padrealumno_alumno.alumno_id '
                                              'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_alumno.padrealumno_id=usuario_padrealumno_padre.padrealumno_id '
                                              'INNER JOIN usuario_padrefam ON usuario_padrealumno_padre.padrefam_id=usuario_padrefam.id '
                                              'INNER JOIN incidencia_incidenciaalumno_alumno  ON usuario_alumno.matricula=incidencia_incidenciaalumno_alumno.alumno_id '
                                              'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_alumno.incidenciaalumno_id  '
                                              'INNER JOIN incidencia_tipoindicencia on incidencia_tipoindicencia.id_tipo=incidencia_incidencia.incidencia_id ')
        return queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset(),
                   'title': 'Lista de alumnos',
                   'year': datetime.now().year,
                   'alumno': 'true',
                   }
        return render(request, self.template_name, context)


def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                model=TipoIndicencia,
                mapdict=['asunto', 'descripcion', 'tipo', 'impacto'])
            return redirect('dashboard:index')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'incidencia/importar_incidencias.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })
