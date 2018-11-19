from datetime import datetime
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse_lazy
from fcm_django.models import FCMDevice
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import alumno
from ProyectSecusoft import settings
from incidencia.serializers import *
from materia.models import Materia
from usuario.models import PadreFam, PadreAlumno, Usuario
from .forms import *
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
    form_class_dos = IndicenciaDocenteForm

    def get_context_data(self, **kwargs):
        context = super(IncidenciaCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.form_class_dos(self.request.GET)
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
        context['incidencias'] = TipoIndicencia.objects.all()
        return context

    def get_success_url(self, **kwargs):
        if kwargs !=  None:
            return reverse_lazy('incidencias:incidencia-nueva-al', kwargs={'pk': self.object.pk,
                                                                           'grado': self.kwargs.get("grado"),
                                                                           'grupo': self.kwargs.get("grupo")})
        else:
            return reverse_lazy('incidencias:incidencia-detalle', args=(self.object.pk,))


class IncidenciaAlCreateView(CreateView):  # Agregar nuevo incidencia
    form_class = IncidenciaAlForm
    template_name = 'incidencia/incidencia_agregar.html'
    form_class_dos = IndicenciaDocenteForm

    def get_context_data(self, **kwargs):
        context = super(IncidenciaAlCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.form_class_dos(self.request.GET)
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

    def get_form_kwargs(self):
        kwargs = super(IncidenciaAlCreateView, self).get_form_kwargs()

        kwargs['grado'] = self.kwargs.get("grado")
        kwargs['grupo'] = self.kwargs.get("grupo")
        kwargs['pk'] = self.kwargs.get("pk")
        return kwargs

    def get_success_url(self):
        if self.request.user.tipo_persona is '1':
            enviar_notificacionT(self.kwargs.get("pk"))
            correo_incidencia(self.kwargs.get("pk"))
            return reverse_lazy('incidencias:incidencia-lista')
        else:
            enviar_notificacion(self.kwargs.get("pk"), self.request.user.id)
            correo_incidencia(self.kwargs.get("pk"))
            return reverse_lazy('dashboard:index')



def enviar_notificacionT(id_incidencia):
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


def enviar_notificacion(id_incidencia, id):
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
    a = IncidenciaDocente.objects.create()
    a.incidencia.add(Incidencia.objects.get(id_incidencia=id_incidencia))
    a.docente.add(Docente.objects.get(docente_id=id))
    print(a)
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
        subject = 'Nueva incidencia: ' + al['incidencias'][x]
        message = 'El alumno: ' + al['alumnos'][x] + ', cometió una falta, para más información ingrese a la aplicación o a la página web ' + " https://secusoft.pythonanywhere.com/login/"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [al['padres'][x], ]
        send_mail(subject, message, email_from, recipient_list)


class IncidenciaTipoCreateView(CreateView):  # Agregar nuevo incidencia
    template_name = 'incidencia/incidencia_agregar.html'
    form_class = IncidenciaTipoForm


class IncidenciaTipoDetailView(DetailView):  # Detalle de un alumno por su id
    template_name = 'incidencia/incidencia_detalle.html'
    model = TipoIndicencia

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(IncidenciaTipoDetailView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = TipoIndicencia.objects.filter(id_tipo=_id)
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['Tipo'] = True
        context['title'] = 'Detalles del tipo de incidencia'
        return context


class IncidenciatipoListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'incidencia/incidencia_lista.html'

    def get_queryset(self):
        queryset = TipoIndicencia.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.tipo_persona is '1':
                context = {'object_list': self.get_queryset(),
                           'title': 'Lista de incidencias',
                           'year': datetime.now().year,
                           'Tipo': 'true',
                           }
                return render(request, self.template_name, context)
            else:
                return HttpResponseRedirect(reverse('dashboard:index'))
        return render(request, self.template_name)


class IncidenciaDetailView(DetailView):  # Detalle de un incidencia por su id
    model = Incidencia
    template_name = 'incidencia/incidencia_detalle.html'

    def get_context_data(self, queryset=None, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = super(IncidenciaDetailView, self).get_context_data(**kwargs)
            _id = self.kwargs.get("pk")
            queryset = Incidencia.objects.raw(
                'Select alumno_alumno.matricula, incidencia_incidencia.*, incidencia_tipoindicencia.* '
                'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                'WHERE incidencia_incidencia.id_incidencia =%s LIMIT 1', [_id])
            queryset2 = Incidencia.objects.raw(
                'Select alumno_alumno.*, incidencia_incidencia.id_incidencia '
                'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                'WHERE incidencia_incidencia.id_incidencia =%s ', [_id])
            if self.request.user.tipo_persona is '2':
                id = self.request.user.id
                docente = Docente.objects.filter(docente_id=id)
                materias = Materia.objects.raw(
                    'SELECT DISTINCT materia_materia.* FROM usuario_docente '
                    'INNER JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
                    'INNER JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
                    'INNER JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
                    'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
                    'WHERE usuario_usuario.id = %s ORDER by materia_materia.grado', [id])
                context['materias'] = materias
                context['grupotutor'] = docente

            context["object"] = queryset
            context["alumnos"] = queryset2
            context['year'] = datetime.now().year
            context['title'] = 'Detalles de incidencia'
            return context

        else:
            return HttpResponseRedirect(reverse('dashboard:index'))


class IncidenciaUpdateView(UpdateView):  # Mofificar un incidencia por su id
    model = Incidencia
    template_name = 'incidencia/incidencia_actualizar.html'
    form_class = IncidenciaForm

    def get_context_data(self, **kwargs):
        context = super(IncidenciaUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['padre'] = True
        context['title'] = 'Editar incidencia'
        return context

    def get_success_url(self):
        return reverse('dashboard:index')


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
        if self.request.user.is_authenticated:
            if self.request.user.tipo_persona is '3':
                padreid = self.request.user.id
                queryset = Incidencia.objects.raw('Select cita_cita.id_cita, alumno_alumno.matricula, alumno_alumno.nombre, alumno_alumno.grado, alumno_alumno.grupo, incidencia_incidencia.*, incidencia_tipoindicencia.* '
                                                  'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                                                  'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                                                  'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                                                  'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                                                  'INNER JOIN usuario_padrealumno_alumno ON alumno_alumno.matricula=usuario_padrealumno_alumno.alumno_id '
                                                  'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_alumno.padrealumno_id=usuario_padrealumno_padre.padrealumno_id '
                                                  'INNER JOIN usuario_padrefam ON usuario_padrealumno_padre.padrefam_id=usuario_padrefam.id '
                                                    'LEFT JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                                                    'LEFT JOIN cita_citaincidencia_cita on cita_citaincidencia_cita.citaincidencia_id = cita_citaincidencia_incidencia.citaincidencia_id '
                                                    'LEFT JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_cita.cita_id '
                                                  'WHERE usuario_padrefam.padre_id =%s', [padreid])

            else:
                queryset = Incidencia.objects.raw('Select cita_cita.id_cita, alumno_alumno.matricula, alumno_alumno.grado, alumno_alumno.grupo, incidencia_incidencia.*, incidencia_tipoindicencia.* '
                                                    'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                                                    'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                                                    'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                                                    'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                                                    'LEFT JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                                                    'LEFT JOIN cita_citaincidencia_cita on cita_citaincidencia_cita.citaincidencia_id = cita_citaincidencia_incidencia.citaincidencia_id '
                                                    'LEFT JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_cita.cita_id ')
            return queryset

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.tipo_persona is '3':
                context = {'object_list': self.get_queryset(),
                           'title': 'Lista de incidencias',
                           'padre': True,
                           'year': datetime.now().year,
                           'alumno': 'true',
                           }
                return render(request, self.template_name, context)
            else:
                context = {'object_list': self.get_queryset(),
                           'title': 'Lista de incidencias',
                           'year': datetime.now().year,
                           'alumno': 'true',
                           }
                return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse('dashboard:index'))


class IncidenciaDownloadView(ListView):  # Mostrar todos lo usuarios
    template_name = 'incidencia/incidencia_descargas.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.tipo_persona is '3':
                padreid = self.request.user.id
                queryset = Incidencia.objects.raw('Select cita_cita.id_cita, alumno_alumno.matricula, alumno_alumno.nombre, alumno_alumno.grado, alumno_alumno.grupo, incidencia_incidencia.*, incidencia_tipoindicencia.* '
                                                  'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                                                  'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                                                  'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                                                  'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                                                  'INNER JOIN usuario_padrealumno_alumno ON alumno_alumno.matricula=usuario_padrealumno_alumno.alumno_id '
                                                  'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_alumno.padrealumno_id=usuario_padrealumno_padre.padrealumno_id '
                                                  'INNER JOIN usuario_padrefam ON usuario_padrealumno_padre.padrefam_id=usuario_padrefam.id '
                                                    'LEFT JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                                                    'LEFT JOIN cita_citaincidencia_cita on cita_citaincidencia_cita.citaincidencia_id = cita_citaincidencia_incidencia.citaincidencia_id '
                                                    'LEFT JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_cita.cita_id '
                                                  'WHERE usuario_padrefam.padre_id =%s', [padreid])

            else:
                queryset = Incidencia.objects.raw('Select cita_cita.id_cita, alumno_alumno.matricula, alumno_alumno.grado, alumno_alumno.grupo, incidencia_incidencia.*, incidencia_tipoindicencia.* '
                                                    'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                                                    'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                                                    'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                                                    'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                                                    'LEFT JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                                                    'LEFT JOIN cita_citaincidencia_cita on cita_citaincidencia_cita.citaincidencia_id = cita_citaincidencia_incidencia.citaincidencia_id '
                                                    'LEFT JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_cita.cita_id ')
            return queryset

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.tipo_persona is '3':
                context = {'object_list': self.get_queryset(),
                           'title': 'Lista de incidencias',
                           'padre': True,
                           'year': datetime.now().year,
                           'alumno': 'true',
                           }
                return render(request, self.template_name, context)
            else:
                context = {'object_list': self.get_queryset(),
                           'title': 'Lista de incidencias',
                           'year': datetime.now().year,
                           'alumno': 'true',
                           }
                return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse('dashboard:index'))


class IncidenciaAlListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'incidencia/incidencia_lista.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.tipo_persona is '2':
                grupo = self.kwargs.get("grupo")
                grado = self.kwargs.get("grado")
                queryset = Incidencia.objects.raw(
                    'Select cita_cita.id_cita, alumno_alumno.matricula, alumno_alumno.grado, alumno_alumno.grupo, incidencia_incidencia.*, incidencia_tipoindicencia.* '
                    'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                    'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                    'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                    'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                    'INNER JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                    'INNER JOIN cita_citaincidencia_cita on cita_citaincidencia_cita.citaincidencia_id = cita_citaincidencia_incidencia.citaincidencia_id '
                    'INNER JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_cita.cita_id '
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

        return HttpResponseRedirect(reverse('dashboard:index'))


class IncidenciaAlUpdateView(UpdateView):  # Mofificar un usuario por su id
    form_class = IncidenciaAlForm
    template_name = 'incidencia/incidencia_agregar.html'

    def get_form_kwargs(self):
        kwargs = super(IncidenciaAlUpdateView, self).get_form_kwargs()
        kwargs['grado'] = self.kwargs.get("grado")
        kwargs['grupo'] = self.kwargs.get("grupo")
        kwargs['pk'] = self.kwargs.get("pk")
        return kwargs

    def get_success_url(self):
        if self.request.user.tipo_persona is '1':
            return reverse_lazy('incidencias:incidencia-lista')
        else:
            return reverse_lazy('dashboard:index')


def import_data(request):
    if request.user.is_authenticated:
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
                'year': datetime.now().year,
            })
    return HttpResponseRedirect(reverse('dashboard:index'))


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(user)
        if user.tipo_persona is '3':
            queryset = PadreAlumno.objects.filter(padre__padre_id=user.pk)
            tok = request.data['tok']
            FCMDevice.objects.get_or_create(registration_id=tok,  user=user, type='android', active=True)
            alumnos = {}
            for a in queryset:
                alumnos = a.alumno.values('matricula'), a.alumno.values('nombre'), a.alumno.values('grado'), a.alumno.values('grupo')
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'alumnos': str(alumnos),
            })
        else:

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })


class IncidenciaView(viewsets.ModelViewSet):
    queryset = Incidencia.objects.all()
    serializer_class = IncidenciaSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = self.kwargs.get("pk")
        incidencia = []
        incidencias = {}
        aaa = []
        incidencia2 ={}
        bbb = []
        queryset = Incidencia.objects.raw(
            'Select alumno_alumno.matricula, alumno_alumno.grado, alumno_alumno.grupo, incidencia_incidencia.*, incidencia_tipoindicencia.*, usuario_usuario.email '
            'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
            'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
            'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
            'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
            'LEFT JOIN incidencia_incidenciadocente_incidencia on incidencia_incidenciadocente_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
            'LEFT JOIN incidencia_incidenciadocente on incidencia_incidenciadocente.id = incidencia_incidenciadocente_incidencia.incidenciadocente_id '
            'LEFT JOIN incidencia_incidenciadocente_docente ON incidencia_incidenciadocente_docente.incidenciadocente_id = incidencia_incidenciadocente.id '
            'LEFT JOIN usuario_docente ON usuario_docente.id = incidencia_incidenciadocente_docente.docente_id '
            'LEFT JOIN usuario_usuario ON usuario_usuario.id = usuario_docente.docente_id '
            'WHERE alumno_alumno.matricula=%s', [user])
        for a in queryset:
            incidencia.append((a.asunto, a.incidencia_id, a.estatus, a.fecha_incidencia.date(), a.observaciones, a.email))
        if len(incidencia) != 0:
            b = len(incidencia)
            for a in incidencia:
                incidencias['id'] = a[1]
                incidencias['estatus'] = a[2]
                incidencias['fecha_incidencia'] = a[3]
                incidencias['asunto'] = a[0]
                incidencias['observaciones'] = a[4]
                incidencias['docente'] = a[5]
                b -= 1
            incidencia2['id'] = [a[1] for a in incidencia]
            incidencia2['estatus'] = [a[2] for a in incidencia]
            incidencia2['fecha_incidencia'] = [a[3] for a in incidencia]
            incidencia2['asunto'] = [a[0] for a in incidencia]
            incidencia2['observaciones'] = [a[4] for a in incidencia]
            incidencia2['docente'] = [a[5] for a in incidencia]
            return Response({'output': incidencia2})
        else:
            return Response({
                'incidencia': 'ninguna',
            })


class TipoIncidenciaView(viewsets.ModelViewSet):
    queryset = TipoIndicencia.objects.all()
    serializer_class = TipoIncidenciaSerializer


class CitaView(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.kwargs.get("pk")
        print(user)
        print(Incidencia.objects.filter(id_incidencia=user))
        queryset = Cita.objects.filter(citaincidencia__incidencia__id_incidencia=user)
        print(queryset)
        for a in queryset.values():
            print(a)
        if queryset:
            return Response({'output': queryset.values()})
        else:
            return Response({
                'incidencia': 'ninguna',
            })


class Logout(APIView):

    def post(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class AvisoView(viewsets.ModelViewSet):
    queryset = Aviso.objects.all()
    serializer_class = AvisoSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.kwargs.get('pk')
        queryset = Aviso.objects.filter(Q(dirigido_a='1') | Q(dirigido_a='3') &
                                        Q(grupo__isnull=True) & Q(grado__isnull=True))
        queryset2 = Aviso.objects.exclude(id__in=queryset.values('id'))
        if queryset2 or queryset:
            alumnos = PadreAlumno.objects.filter(padre__padre_id=user)
            av = []
            avs = {}
            incidencia2 ={}
            for a in queryset:
                av.append((a.asunto, a.id, a.descripcion, a.fecha_creacion.date()))
                if len(av) != 0:
                    b = len(av)
                    for a in av:
                        avs['id'] = a[1]
                        avs['asunto'] = a[0]
                        avs['fecha_creacion'] = a[3]
                        avs['descripcion'] = a[2]
                        b -= 1
                    incidencia2['id'] = [a[1] for a in av]
                    incidencia2['asunto'] = [a[0] for a in av]
                    incidencia2['fecha_creacion'] = [a[3] for a in av]
                    incidencia2['descripcion'] = [a[2] for a in av]
            for a in queryset2:
                if a.grupo is not None and a.grado is not None and a.dirigido_a == '3':
                    for i in alumnos:
                        l = 0
                        if i.alumno.values('grado')[l]['grado'] == a.grado \
                                and i.alumno.values('grupo')[l]['grupo'] == a.grupo:
                            av.append((a.asunto, a.id, a.descripcion, a.fecha_creacion.date()))
                        l += 1
                elif a.grupo is not None and a.grado is None and a.dirigido_a == '3':
                    for i in alumnos:
                        l = 0
                        if i.alumno.values('grupo')[l]['grupo'] == a.grupo:
                            av.append((a.asunto, a.id, a.descripcion, a.fecha_creacion.date()))
                        l += 1
                elif a.grupo is None and a.grado is not None and a.dirigido_a == '3':
                    for i in alumnos:
                        l = 0
                        if i.alumno.values('grado')[l]['grado'] == a.grado:
                            av.append((a.asunto, a.id, a.descripcion, a.fecha_creacion.date()))
                        l += 1
                if len(av) != 0:
                    b = len(av)
                    for f in av:
                        avs['id'] = f[1]
                        avs['asunto'] = f[0]
                        avs['fecha_creacion'] = f[3]
                        avs['descripcion'] = f[2]
                        b -= 1
                    incidencia2['id'] = [o[1] for o in av]
                    incidencia2['asunto'] = [o[0] for o in av]
                    incidencia2['fecha_creacion'] = [o[3] for o in av]
                    incidencia2['descripcion'] = [o[2] for o in av]
            return Response({'output': incidencia2})

        else:
            return Response({
                'avisos': 'ninguno',
            })
