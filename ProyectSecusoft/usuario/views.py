import itertools
from datetime import datetime
from django.shortcuts import reverse, get_object_or_404, get_list_or_404, render
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
user = get_user_model()


class UsuarioListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'usuario/usuario_lista.html'
    queryset = Persona.objects.exclude(tipo_persona='4')

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
    queryset = Persona.objects.filter(tipo_persona='3')

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
    # queryset1 = Alumno.objects.all()
    # queryset2 = Persona.objects.filter(id__in=queryset1.values('alumno_id'))
    # queryset = PadreAlumno.objects.filter(alumno__in=queryset1.values('matricula'))
    # for a in queryset:
    #     print(a)

    def get_queryset(self):
        if self.request.user.usuario.tipo_persona is '3':
            print("Padre de femilia")
            padreid = self.request.user.usuario_id
            print(padreid)
            queryset = Alumno.objects.raw(
                'Select usuario_alumno.*, usuario_persona.*, usuario_padrealumno_alumno.padrealumno_id, usuario_padrealumno_padre.padrefam_id, usuario_padrefam.padre_id '
                'FROM usuario_alumno INNER JOIN usuario_persona ON usuario_alumno.alumno_id=usuario_persona.id '
                'INNER JOIN usuario_padrealumno_alumno ON usuario_alumno.matricula=usuario_padrealumno_alumno.alumno_id '
                'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_alumno.padrealumno_id=usuario_padrealumno_padre.padrealumno_id  '
                'INNER JOIN usuario_padrefam ON usuario_padrealumno_padre.padrefam_id=usuario_padrefam.id WHERE usuario_padrefam.padre_id=%s', [padreid])
        else:
            print("no es padre de familia")
            queryset = Alumno.objects.raw(
            'Select usuario_alumno.*, usuario_persona.*, usuario_padrealumno_alumno.padrealumno_id, usuario_padrealumno_padre.padrefam_id, usuario_padrefam.padre_id '
            'FROM usuario_alumno INNER JOIN usuario_persona ON usuario_alumno.alumno_id=usuario_persona.id '
            'INNER JOIN usuario_padrealumno_alumno ON usuario_alumno.matricula=usuario_padrealumno_alumno.alumno_id '
            'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_alumno.padrealumno_id=usuario_padrealumno_padre.padrealumno_id  '
            'INNER JOIN usuario_padrefam ON usuario_padrealumno_padre.padrefam_id=usuario_padrefam.id')
        return queryset

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
    template_name = 'usuario/usuario_agregar.html'
    form_class = PersonaForm
    segundo_form_class = AlumnoForm

    def get_context_data(self, **kwargs):
        context = super(PersonaAlumnoCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['alumno'] = True
        context['title'] = 'Agregar Alumno'
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
            alumno = form2.save(commit=False)
            persona.tipo_persona = '4'
            persona.save()
            alumno.alumno = persona
            alumno.save()
            return HttpResponseRedirect('../alumnos')
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
    segundo_form_class = PadreAlumnoForm
    tercer_form_class = RegisterForm
    cuarto_form_class = PadreForm

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
        context['year'] = datetime.now().year
        context['padre'] = True
        context['title'] = 'Agregar Padre de familia'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form_class(request.POST)
        form3 = self.tercer_form_class(request.POST)
        form4 = self.cuarto_form_class(request.POST)
        if form.is_valid():
            print("Form valido")
        if form2.is_valid():
            print("form2 valido")
        if form3.is_valid():
            print("Form3 valido")
        if form4.is_valid():
            print("Form4 valido")
        if form.is_valid() and form3.is_valid() and form4.is_valid():
            print("Formularios validos ")
            persona = form.save(commit=False)
            usuario = form3.save(commit=False)
            padrefam = form4.save(commit=False)
            persona.tipo_persona = '3'
            persona.save()
            padrefam.padre = persona
            padrefam.save()
            usuario.usuario = persona
            usuario.save()
            padrealumno = form2.save(commit=False)
            padrealumno.save()
            padrealumno.padre.add(padrefam)
            padrealumno.alumno.add(request.POST['alumno'])
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
    tercer_form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super(UsuarioDocenteCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.tercer_form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['docente'] = True
        context['title'] = 'Agregar Docente'
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
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            print("Formularios validos ")
            persona = form.save(commit=False)
            docente = form2.save(commit=False)
            usuario = form3.save(commit=False)
            persona.tipo_persona = '2'
            persona.save()
            docente.docente = persona
            docente.save()
            usuario.usuario = persona
            usuario.active = True
            usuario.save()
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UsuarioDetailView(DetailView):  # Detalle de un usuario por su id
    template_name = 'usuario/usuario_detalle.html'
    model = Persona

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(UsuarioDetailView, self).get_context_data(*args, **kwargs)
        _id = self.kwargs.get("pk")
        queryset = Persona.objects.filter(id=_id)
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['usuario'] = True
        context['title'] = 'Detalles del usuario'
        return context


class AlumnoDetailView(DetailView):  # Detalle de un alumno por su id
    template_name = 'usuario/usuario_detalle.html'
    model = Alumno

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(AlumnoDetailView, self).get_context_data(*args, **kwargs)
        _id = self.kwargs.get("pk")
        queryset1 = Alumno.objects.filter(matricula=_id)
        queryset = Persona.objects.filter(id__in=queryset1.values('alumno_id'))
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['Alumno'] = True
        context['title'] = 'Detalles del alumno'
        return context


class DocenteDetailView(DetailView):  # Detalle de un alumno por su id
    template_name = 'usuario/usuario_detalle.html'
    model = Persona

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(DocenteDetailView, self).get_context_data(*args, **kwargs)
        _id = self.kwargs.get("pk")
        queryset = Persona.objects.filter(id=_id)
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['usuario'] = True
        context['title'] = 'Detalles del usuario'
        return context


class UsuarioUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'usuario/usuario_actualizar.html'
    form_class = PersonaForm
    segundo_form_class = PadreAlumnoForm
    tercer_form_class = RegisterForm
    cuarto_form_class = PadreForm
    model = Persona

    def get_context_data(self, **kwargs):
        context = super(UsuarioUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.tercer_form_class(self.request.GET)
        if 'form4' not in context:
            context['form4'] = self.cuarto_form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['padre'] = True
        context['title'] = 'Agregar Padre de familia'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form_class(request.POST)
        form3 = self.tercer_form_class(request.POST)
        form4 = self.cuarto_form_class(request.POST)
        if form.is_valid():
            print("Form valido")
        if form2.is_valid():
            print("form2 valido")
        if form3.is_valid():
            print("Form3 valido")
        if form4.is_valid():
            print("Form4 valido")
        if form.is_valid() and form3.is_valid() and form4.is_valid():
            print("Formularios validos ")
            persona = form.save(commit=False)
            usuario = form3.save(commit=False)
            padrefam = form4.save(commit=False)
            persona.tipo_persona = '3'
            persona.save()
            padrefam.padre = persona
            padrefam.save()
            usuario.usuario = persona
            usuario.save()
            padrealumno = form2.save(commit=False)
            padrealumno.save()
            padrealumno.padre.add(padrefam)
            padrealumno.alumno.add(request.POST['alumno'])
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))

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


class AlumnoUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'usuario/usuario_actualizar.html'
    model = Alumno
    form_class = AlumnoForm

    def get_context_data(self, **kwargs):
        context = super(AlumnoUpdateView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset1 = Alumno.objects.filter(matricula=_id)
        queryset = Persona.objects.filter(id__in=queryset1.values('alumno_id'))
        context["object"] = queryset
        context["object2"] = queryset1
        context["form2"] = PersonaForm
        context['year'] = datetime.now().year
        context['Alumno'] = True
        context['title'] = 'Detalles del alumno'
        return context
