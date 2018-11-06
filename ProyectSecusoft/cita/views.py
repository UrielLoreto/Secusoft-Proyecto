from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from fcm_django.models import FCMDevice

from ProyectSecusoft import settings
from alumno.models import Alumno
from materia.models import Materia
from usuario.models import Usuario
from .forms import *
from django.contrib import messages
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)


class CitaIncidenciaCreateView(CreateView):  # Agregar nuevo incidencia
    template_name = 'cita/cita_agregar.html'
    form_class = CitaIncidenciaForm
    segundo_form_class = IncidenciaForm

    def get_context_data(self, **kwargs):
        context = super(CitaIncidenciaCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.segundo_form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['title'] = 'Agregar incidencia'
        context['incidencia'] = True
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.segundo_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            print("Formularios validos ")
            cita = form.save(commit=False)
            citaincidencia = form2.save(commit=False)
            cita.save()
            citaincidencia.save()
            citaincidencia.cita.add(cita)
            citaincidencia.incidencia.add(request.POST['incidencia'])
            return HttpResponseRedirect('..')
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def form_valid(self, form):
        return super().form_valid(form)


class CitaIncidenciaAlCreateView(CreateView):  # Agregar nuevo incidencia
    template_name = 'cita/cita_agregar.html'
    form_class = CitaIncidenciaForm

    def get_context_data(self, **kwargs):
        context = super(CitaIncidenciaAlCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        id = self.request.user.id
        materias = Materia.objects.raw(
            'SELECT DISTINCT materia_materia.* FROM usuario_docente '
            'INNER JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
            'INNER JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
            'INNER JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
            'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
            'WHERE usuario_usuario.id = %s ORDER by materia_materia.grado', [id])
        context['materias'] = materias
        context['year'] = datetime.now().year
        context['title'] = 'Agregar incidencia'
        return context

    def get_success_url(self, **kwargs):
        if kwargs != None:
            return reverse_lazy('citas:cita-incidencia-nueva-al-cit', kwargs={'pk': self.object.pk, 'grado': self.kwargs.get("grado"), 'grupo': self.kwargs.get("grupo")})
        else:
            return reverse_lazy('citas:cita-incidencia-detalle', args=(self.object.pk,))


class IncidenciaAlCreateView(CreateView):  # Agregar nuevo incidencia
    form_class = CitaIncidenciaAlForm
    template_name = 'cita/cita_agregar.html'

    def get_form_kwargs(self):
        kwargs = super(IncidenciaAlCreateView, self).get_form_kwargs()
        kwargs['grado'] = self.kwargs.get("grado")
        kwargs['grupo'] = self.kwargs.get("grupo")
        kwargs['pk'] = self.kwargs.get("pk")
        return kwargs

    def get_success_url(self):
        if self.request.user.tipo_persona is '1':
            enviar_notificacion(self.kwargs.get("pk"))
            correo_incidencia(self.kwargs.get("pk"))
            return reverse_lazy('incidencias:incidencia-lista')
        else:
            enviar_notificacion(self.kwargs.get("pk"))
            correo_incidencia(self.kwargs.get("pk"))
            return reverse_lazy('dashboard:index')


def enviar_notificacion(id_incidencia):
    incidencia = TipoIndicencia.objects.raw(
        'SELECT incidencia_tipoindicencia.* FROM incidencia_incidenciaalumno '
        'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno.id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.incidenciaalumno_id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidencia on incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
        'INNER JOIN incidencia_tipoindicencia on incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
        'INNER JOIN alumno_alumno on alumno_alumno.matricula = incidencia_incidenciaalumno_alumno.alumno_id '
        'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
        'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
        'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
        'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
        'WHERE incidencia_incidenciaalumno_incidencia.incidencia_id = %s', [id_incidencia])
    alumnos = Alumno.objects.raw(
        'SELECT alumno_alumno.nombre, alumno_alumno.matricula, usuario_usuario.email, incidencia_incidencia.*, incidencia_tipoindicencia.asunto FROM incidencia_incidenciaalumno '
        'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno.id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.incidenciaalumno_id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidencia on incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
        'INNER JOIN incidencia_tipoindicencia on incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
        'INNER JOIN alumno_alumno on alumno_alumno.matricula = incidencia_incidenciaalumno_alumno.alumno_id '
        'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
        'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
        'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
        'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
        'WHERE incidencia_incidenciaalumno_incidencia.incidencia_id = %s', [id_incidencia])
    padres = Usuario.objects.raw(
        'SELECT usuario_usuario.* FROM incidencia_incidenciaalumno '
        'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno.id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.incidenciaalumno_id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidencia on incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
        'INNER JOIN incidencia_tipoindicencia on incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
        'INNER JOIN alumno_alumno on alumno_alumno.matricula = incidencia_incidenciaalumno_alumno.alumno_id '
        'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
        'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
        'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
        'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
        'WHERE incidencia_incidenciaalumno_incidencia.incidencia_id = %s', [id_incidencia])
    al = {}
    al['alumnos'] = [o.nombre for o in alumnos]
    num = len(al['alumnos'])
    al['padres'] = [o.id for o in padres]
    al['incidencias'] = [o.asunto for o in incidencia]
    for x in range(num):
        device = FCMDevice.objects.filter(user=al['padres'][x])
        print(device)
        device.send_message(title="Incidencia nueva: " + al['incidencias'][x], body="Alumno: " + al['alumnos'][x])


def correo_incidencia(id_incidencia):
    incidencia = TipoIndicencia.objects.raw(
        'SELECT incidencia_tipoindicencia.* FROM incidencia_incidenciaalumno '
        'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno.id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.incidenciaalumno_id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidencia on incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
        'INNER JOIN incidencia_tipoindicencia on incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
        'INNER JOIN alumno_alumno on alumno_alumno.matricula = incidencia_incidenciaalumno_alumno.alumno_id '
        'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
        'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
        'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
        'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
        'WHERE incidencia_incidenciaalumno_incidencia.incidencia_id = %s', [id_incidencia])
    alumnos = Alumno.objects.raw(
        'SELECT alumno_alumno.nombre, alumno_alumno.matricula, usuario_usuario.email, incidencia_incidencia.*, incidencia_tipoindicencia.asunto FROM incidencia_incidenciaalumno '
        'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno.id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.incidenciaalumno_id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidencia on incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
        'INNER JOIN incidencia_tipoindicencia on incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
        'INNER JOIN alumno_alumno on alumno_alumno.matricula = incidencia_incidenciaalumno_alumno.alumno_id '
        'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
        'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
        'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
        'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
        'WHERE incidencia_incidenciaalumno_incidencia.incidencia_id = %s', [id_incidencia])
    padres = Usuario.objects.raw(
        'SELECT usuario_usuario.* FROM incidencia_incidenciaalumno '
        'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno.id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.incidenciaalumno_id = incidencia_incidenciaalumno_incidencia.incidenciaalumno_id '
        'INNER JOIN incidencia_incidencia on incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
        'INNER JOIN incidencia_tipoindicencia on incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
        'INNER JOIN alumno_alumno on alumno_alumno.matricula = incidencia_incidenciaalumno_alumno.alumno_id '
        'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
        'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
        'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
        'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
        'WHERE incidencia_incidenciaalumno_incidencia.incidencia_id = %s', [id_incidencia])
    al = {}
    al['alumnos'] = [o.nombre for o in alumnos]
    num = len(al['alumnos'])
    al['padres'] = [o.email for o in padres]
    al['incidencias'] = [o.asunto for o in incidencia]
    for x in range(num):
        subject = 'Nueva incidencia' + al['incidencias'][x]
        message = 'El alumno' + al['alumnos'][x] + ' cometió una falta, para más información ingrese a la aplicación o a la página web' + "https://secusoft.pythonanywhere.com/login/"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [al['padres'][x], ]
        send_mail(subject, message, email_from, recipient_list)


class CitaIncidenciaDetailView(DetailView):  # Detalle de un incidencia por su id
    model = Cita
    template_name = 'cita/cita_detalle.html'

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(CitaIncidenciaDetailView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = Cita.objects.raw('Select cita_cita.*, incidencia_incidencia.id_incidencia as idincidencia, incidencia_tipoindicencia.asunto as asunto2, cita_cita.* from alumno_alumno '
                                          'INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                                          'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                                          'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                                          'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                                          'INNER JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                                          'INNER JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_incidencia.citaincidencia_id '
                                          'WHERE cita_cita.id_cita = %s GROUP BY cita_cita.id_cita', [_id])
        queryset2 = Incidencia.objects.raw(
            'Select alumno_alumno.matricula, incidencia_incidencia.id_incidencia '
            'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
            'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
            'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
            'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
            'WHERE incidencia_incidencia.id_incidencia =%s ', [_id])
        # queryset2 = Cita.objects.filter(matricula__in=[o.matricula for o in self.get_queryset()])
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['title'] = 'Detalles de incidencia'
        return context


class CitaIncidenciaUpdateView(UpdateView):  # Mofificar un incidencia por su id
    model = Incidencia
    template_name = 'cita/cita_actualizar.html'
    form_class = IncidenciaForm

    def get_object(self, queryset=None):
        _id = self.kwargs.get("id")
        return get_object_or_404(Incidencia, id_incidencia=_id)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class CitaIncidenciaListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'cita/cita_lista.html'

    def get_queryset(self):
        if self.request.user.tipo_persona is '3':
            padreid = self.request.user.id
            queryset = Cita.objects.raw('Select cita_cita.*, incidencia_incidencia.id_incidencia '
                                              'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                                              'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                                              'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                                              'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                                              'INNER JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                                              'INNER JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_incidencia.citaincidencia_id '
                                              'INNER JOIN usuario_padrealumno_alumno ON alumno_alumno.matricula=usuario_padrealumno_alumno.alumno_id '
                                              'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_alumno.padrealumno_id=usuario_padrealumno_padre.padrealumno_id '
                                              'INNER JOIN usuario_padrefam ON usuario_padrealumno_padre.padrefam_id=usuario_padrefam.id '
                                              'WHERE usuario_padrefam.padre_id =%s', [padreid])
            return queryset
        if self.request.user.tipo_persona is '1':
            queryset = Cita.objects.raw('Select cita_cita.*, incidencia_incidencia.id_incidencia '
                                              'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                                              'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                                              'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                                              'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                                              'INNER JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                                              'INNER JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_incidencia.citaincidencia_id GROUP BY cita_cita.id_cita')
            return queryset

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.tipo_persona is '3':
                context = {'object_list': self.get_queryset(),
                           'title': 'Lista de citas',
                           'padre': True,
                           'year': datetime.now().year,
                           'alumno': 'true',
                           }
            else:
                context = {'object_list': self.get_queryset(),
                           'title': 'Lista de citas',
                           'year': datetime.now().year,
                           'alumno': 'true',
                           }
            return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse('dashboard:index'))


class CitaIncidenciaAlListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'cita/cita_lista.html'

    def get_queryset(self):
        if self.request.user.tipo_persona is '2':
            grupo = self.kwargs.get("grupo")
            grado = self.kwargs.get("grado")
            queryset = Cita.objects.raw(
            'Select cita_cita.* '
            'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
            'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
            'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
            'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
            'INNER JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
            'INNER JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_incidencia.citaincidencia_id '
            'WHERE alumno_alumno.grado = %s and alumno_alumno.grupo = %s ', [grado, grupo])
            return queryset

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.tipo_persona is '2':
                id = self.request.user.id
                materias = Materia.objects.raw(
                    'SELECT DISTINCT materia_materia.* FROM usuario_docente '
                    'INNER JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
                    'INNER JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
                    'INNER JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
                    'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
                    'WHERE usuario_usuario.id = %s ORDER by materia_materia.grado', [id])
                context = {'object_list': self.get_queryset(),
                           'title': 'Lista de incidencias',
                           'materias': materias,
                           'year': datetime.now().year,
                           'alumno': 'true',
                           }
                return render(request, self.template_name, context)
            context = {'object_list': self.get_queryset(),
                       'title': 'Lista de citas',
                       'year': datetime.now().year,
                       'alumno': 'true',
                       }
            return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse('dashboard:index'))
