import django_excel as excel
from datetime import datetime
from django.shortcuts import reverse, get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from materia.models import Materia
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    FormView,
    UpdateView
)
user = get_user_model()


class UsuarioListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'usuario/usuario_lista.html'
    queryset = Usuario.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {
            'object_list': self.get_queryset(),
            'title': 'Lista de usuarios',
            'year': datetime.now().year,
        }
        return render(request, self.template_name, context)


class PadreListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'usuario/usuario_lista.html'
    queryset = Usuario.objects.filter(tipo_persona='3')

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset(),
                   'title': 'Lista de usuarios',
                   'year': datetime.now().year,
                   'padref': True,
                   }
        return render(request, self.template_name, context)


class DocenteListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'usuario/usuario_lista.html'
    queryset = Usuario.objects.filter(tipo_persona='2')

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset(),
                   'title': 'Lista de docentes',
                   'year': datetime.now().year,
                   'docente': True,
                   }
        return render(request, self.template_name, context)


class UsuarioPadreCreateView(CreateView):  # Agregar nuevo padre
    template_name = 'usuario/usuario_agregar.html'
    form_class = PersonaForm
    segundo_form_class = PadreAlumnoForm
    tercer_form_class = PadreForm

    def get_context_data(self, **kwargs):
        context = super(UsuarioPadreCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.tercer_form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['padre'] = True
        context['title'] = 'Agregar Padre de familia'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form_class(request.POST)
        form3 = self.tercer_form_class(request.POST)
        if form.is_valid():
            print("Form valido")
        if form2.is_valid():
            print("form2 valido")
        if form3.is_valid():
            print("Form3 valido")
        if form.is_valid() and form3.is_valid():
            print("Formularios validos ")
            persona = form.save(commit=False)
            padrefam = form3.save(commit=False)
            persona.tipo_persona = '3'
            persona.set_password(request.POST["password1"])
            persona.save()
            padrefam.padre = persona
            padrefam.save()
            padrealumno = form2.save(commit=False)
            padrealumno.save()
            for a in request.POST['alumno']:
                print(a)
            padrealumno.alumno.add(request.POST['alumno'])
            padrealumno.padre.add(padrefam)
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UsuarioDocenteCreateView(CreateView):  # Agregar nuevo padre
    template_name = 'usuario/usuario_agregar.html'
    form_class = PersonaForm
    segundo_form_class = DocenteForm

    def get_context_data(self, **kwargs):
        context = super(UsuarioDocenteCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['docente'] = True
        context['title'] = 'Agregar Docente'
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
            persona.tipo_persona = '2'
            persona.save()
            docente.docente = persona
            docente.save()
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UsuarioDetailView(DetailView):  # Detalle de un usuario por su id
    template_name = 'usuario/usuario_detalle.html'
    model = Usuario

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(UsuarioDetailView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        context['id'] = _id
        queryset = Usuario.objects.filter(id=_id)
        tipo = queryset.values('tipo_persona')[0]
        if tipo['tipo_persona'] == '1':
            print("admin")
        elif tipo['tipo_persona'] == '2':
            docente = Docente.objects.filter(docente_id=_id)
            print(docente.values('tutor'))
            tutor = docente.values('tutor')
            if tutor[0]['tutor'] == '1':
                grupo = docente.values('grupo')
                grupotutorado = Alumno.objects.filter(grupo=grupo[0]['grupo'])
                print(grupo[0]['grupo'])

            queryset1 = Materia.objects.raw(
                'SELECT materia_materia.*, materia_materiadocente_docente.*, usuario_docente.* '
                'From materia_materia '
                'Inner join materia_materiadocente_docente on materia_materia.id=materia_materiadocente_docente.materiadocente_id '
                'Inner join usuario_docente on materia_materiadocente_docente.docente_id=usuario_docente.id '
                'where usuario_docente.docente_id=%s', [_id])
            context["object_list"] = queryset1
        elif tipo['tipo_persona'] == '3':
            context['padre'] = True
            for b in queryset:
                padreid = b.pk
                queryset1 = Alumno.objects.raw(
                    'SELECT alumno_alumno.*, usuario_usuario.id, usuario_usuario.nombre as nombre2, usuario_usuario.apellido as apellido2 FROM alumno_alumno '
                    'INNER JOIN usuario_padrealumno_alumno ON usuario_padrealumno_alumno.alumno_id=alumno_alumno.matricula '
                    'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_padre.padrealumno_id=usuario_padrealumno_alumno.padrealumno_id '
                    'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
                    'INNER JOIN usuario_usuario ON usuario_usuario.id=usuario_padrefam.padre_id WHERE usuario_padrefam.padre_id=%s',
                    [padreid])
                context["object_list"] = queryset1
                queryset1 = PadreFam.objects.filter(padre_id=padreid)
                queryse2 = PadreAlumno.objects.filter(padre__in=queryset1.values('id'))
                c = queryse2
            for d in c:
                context["id_padre"] = d.id

        context["object"] = queryset
        context['year'] = datetime.now().year
        context['usuario'] = True
        context['title'] = 'Detalles del usuario'
        return context


class DocenteDetailView(DetailView):  # Detalle de un alumno por su id
    template_name = 'usuario/usuario_detalle.html'
    model = Usuario

    def get_context_data(self, queryset=None, **kwargs):
        context = super(DocenteDetailView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = Usuario.objects.filter(id=_id)
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['usuario'] = True
        context['title'] = 'Detalles del usuario'
        return context


class UsuarioPadreUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'usuario/usuario_actualizar.html'
    form_class = PersonaActForm
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super(UsuarioPadreUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['title'] = 'Editar Padre de familia'
        return context


class PadreAlumnoUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'usuario/usuario_actualizar.html'
    form_class = PadreAlumnoForm
    model = PadreAlumno

    def get_context_data(self, **kwargs):
        context = super(PadreAlumnoUpdateView, self).get_context_data(**kwargs)
        if 'formp' not in context:
            context['formp'] = self.form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['padre'] = True
        context['title'] = 'Editar Padre alumnos de familia'
        return context

    def get_success_url(self):
        return reverse('usuarios:usuario-lista-padre')


class UsuarioDocenteUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'usuario/usuario_actualizar.html'
    form_class = PersonaForm
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super(UsuarioDocenteUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['title'] = 'Editar Docente'
        return context


class UsuarioDeleteView(DeleteView):  # Eliminar un usuario por su id
    template_name = 'usuario/usuario_eliminar.html'

    def get_object(self, queryset=None):
        _id = self.kwargs.get("id")
        return get_object_or_404(Usuario, id_persona=_id)

    def get_success_url(self):
        return reverse('usuarios:usuario-lista')


def PerilUsuario(request):
    template_name = 'usuario/usuario_detalle.html'
    id = request.user.get_id()
    queryset = Usuario.objects.filter(id=id)
    args = {'user': request.user,
            'object': queryset,
            'year': datetime.now().year,
            'title': 'Detalles del usuario',
            'perfil': True,
            'usuario': True}
    return render(request, template_name, args)


class PerilUsuarioUpdate(UpdateView):  # Mofificar un usuario por su id
    template_name = 'usuario/usuario_perfil_actualizar.html'
    form_class = PersonaForm
    model = Usuario

    def get_object(self):
        usuario = self.request.user.get_id()
        return get_object_or_404(Usuario, pk=usuario)

    def get_success_url(self):
        child = self.get_object()
        return reverse('usuarios:usuario-perfil')

    def get_context_data(self, **kwargs):
        context = super(PerilUsuarioUpdate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['title'] = 'Modificar datos del usuario'
        context['perfil'] = True
        return context


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Tu contraseña se cambio corrrectamente')
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Por favor, corrija el error a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usuario/usuario_perfil_contra.html', {
        'form': form,
        'year': datetime.now().year,
        'title': 'Cambio de contraseña',
    })

