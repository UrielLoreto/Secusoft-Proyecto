from datetime import datetime
from django.shortcuts import reverse, get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import *
from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    FormView,
    UpdateView
)
# Create your views here.


class AlumnoCreateView(CreateView):  # Agregar nuevo alumno
    template_name = 'alumno/alumno_agregar.html'
    form_class = AlumnoForm

    def get_context_data(self, **kwargs):
        context = super(AlumnoCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['alumno'] = True
        context['title'] = 'Agregar Alumno'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            print("Form valido")
        if form.is_valid():
            print("Formularios validos ")
            alumno = form.save(commit=False)
            alumno.save()
            return HttpResponseRedirect('', alumno.matricula)
        else:
            print("MAL")
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class AlumnoDetailView(DetailView):  # Detalle de un alumno por su id
    template_name = 'alumno/alumno_detalle.html'
    model = Alumno

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(AlumnoDetailView, self).get_context_data(**kwargs)
        queryset = Alumno.objects.all()
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['Alumno'] = True
        context['title'] = 'Detalles del alumno'
        return context


class AlumnoUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'alumno/alumno_actualizar.html'
    model = Alumno
    form_class = AlumnoActForm

    def get_context_data(self, **kwargs):
        context = super(AlumnoUpdateView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = Alumno.objects.filter(matricula=_id)
        print(queryset)
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['title'] = 'Detalles del alumno'
        return context


class AlumnoListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'alumno/alumno_lista.html'
    # queryset1 = Alumno.objects.all()
    # queryset2 = Usuario.objects.filter(id__in=queryset1.values('alumno_id'))
    # queryset = PadreAlumno.objects.filter(alumno__in=queryset1.values('matricula'))
    # for a in queryset:
    #     print(a)

    def get_queryset(self):
        if self.request.user.tipo_persona is '3':
            print("Padre de femilia")
            padreid = self.request.user.usuario_id
            print(padreid)
            queryset = Alumno.objects.raw('SELECT alumno_alumno.*, usuario_usuario.id, usuario_usuario.nombre as nombre2, usuario_usuario.apellido as apellido2 FROM alumno_alumno '
                                          'INNER JOIN usuario_padrealumno_alumno ON usuario_padrealumno_alumno.alumno_id=alumno_alumno.matricula '
                                          'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_padre.padrealumno_id=usuario_padrealumno_alumno.padrealumno_id '
                                          'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
                                          'INNER JOIN usuario_usuario ON usuario_usuario.id=usuario_padrefam.padre_id WHERE usuario_padrefam.padre_id=%s', [padreid])
        else:
            print("no es padre de familia")
            queryset = Alumno.objects.raw('SELECT alumno_alumno.*, usuario_usuario.id, usuario_usuario.nombre as nombre2, usuario_usuario.apellido as apellido2 FROM alumno_alumno '
                                          'INNER JOIN usuario_padrealumno_alumno ON usuario_padrealumno_alumno.alumno_id=alumno_alumno.matricula '
                                          'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_padre.padrealumno_id=usuario_padrealumno_alumno.padrealumno_id '
                                          'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
                                          'INNER JOIN usuario_usuario ON usuario_usuario.id=usuario_padrefam.padre_id')
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

        def choice_func(row):
            q = Alumno.objects.filter(id=row[0])[0]
            row[0] = q
            print(q)
            return row
        if form.is_valid():
            print(request.FILES['file'].get_array())
            for a in request.FILES['file'].iget_array():
                print(a)
            # request.FILES['file'].save_book_to_database(
            #     models=[Usuario, Alumno],
            #     initializers=[None, choice_func],
            #     mapdicts=[
            #         ['nombre', 'apellido', 'tipo_persona', 'sexo', 'fecha_nacimiento'],
            #         ['matricula', 'grado', 'grupo']]
            # )
            return redirect('dashboard:index')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'usuario/importar_alumnos.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })
