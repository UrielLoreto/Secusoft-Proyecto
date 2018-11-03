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
        if self.request.user.tipo_persona is '2':
            print("Docente")
            doceente = self.request.user.id
            queryset = Materia.objects.raw(
                'SELECT materia_materia.*, materia_materiadocente_docente.*, usuario_docente.* '
                'From materia_materia '
                'Inner join materia_materiadocente_docente on materia_materia.id=materia_materiadocente_docente.materiadocente_id '
                'Inner join usuario_docente on materia_materiadocente_docente.docente_id=usuario_docente.id '
                'where usuario_docente.docente_id=%s', [doceente])
            return queryset

        elif self.request.user.tipo_persona is '1':
            queryset = Materia.objects.raw(
                'SELECT materia_materia.*, materia_materiadocente_docente.*, usuario_docente.* '
                'From materia_materia '
                'LEFT join materia_materiadocente_docente on materia_materia.id=materia_materiadocente_docente.materiadocente_id '
                'LEFT join usuario_docente on materia_materiadocente_docente.docente_id=usuario_docente.id')
            return queryset

    def get(self, request, *args, **kwargs):
        id = self.request.user.id
        materias = Materia.objects.raw(
            'SELECT DISTINCT materia_materia.* FROM usuario_docente '
            'LEFT JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
            'LEFT JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
            'LEFT JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
            'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
            'WHERE usuario_usuario.id = %s ORDER by materia_materia.id', [id])
        context = {
            'object_list': self.get_queryset(),
            'materias': materias,
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

#
# class MateriaDetailView(DetailView):  # Detalle de un alumno por su id
#     template_name = 'alumno/alumno_detalle.html'
#     model = Alumno
#
#     def get_context_data(self, queryset=None, *args, **kwargs):
#         context = super(AlumnoDetailView, self).get_context_data(**kwargs)
#         _id = self.kwargs.get("pk")
#         queryset = Alumno.objects.filter(matricula=_id)
#         queryset2 = Alumno.objects.raw(
#             'SELECT alumno_alumno.*, usuario_usuario.id, usuario_usuario.nombre as nombre2, usuario_usuario.apellido as apellido2 FROM alumno_alumno '
#             'INNER JOIN usuario_padrealumno_alumno ON usuario_padrealumno_alumno.alumno_id=alumno_alumno.matricula '
#             'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_padre.padrealumno_id=usuario_padrealumno_alumno.padrealumno_id '
#             'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
#             'INNER JOIN usuario_usuario ON usuario_usuario.id=usuario_padrefam.padre_id '
#             'WHERE alumno_alumno.matricula=%s', [_id])
#         context["object"] = queryset
#         context["padre"] = queryset2
#         context['year'] = datetime.now().year
#         context['Alumno'] = True
#         context['title'] = 'Detalles del alumno'
#         return context
#
#
# class MateriaUpdateView(UpdateView):  # Mofificar un usuario por su id
#     template_name = 'alumno/alumno_actualizar.html'
#     model = Alumno
#     form_class = AlumnoActForm
#
#     def get_context_data(self, **kwargs):
#         context = super(AlumnoUpdateView, self).get_context_data(**kwargs)
#         _id = self.kwargs.get("pk")
#         queryset = Alumno.objects.filter(matricula=_id)
#         print(queryset)
#         context["object"] = queryset
#         context['year'] = datetime.now().year
#         context['title'] = 'Detalles del alumno'
#         return context
