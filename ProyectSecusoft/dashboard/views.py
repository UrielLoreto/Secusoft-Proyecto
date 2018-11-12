from django.shortcuts import render
from datetime import datetime
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from fcm_django.models import FCMDevice
from alumno.models import Alumno
from dashboard.models import Aviso
from materia.models import Materia
from usuario.models import Docente, Usuario
from .forms import LoginForm, AvisoForm
from django.http import HttpResponseRedirect
from django.views.generic import (
    FormView, DetailView,
    CreateView, ListView, UpdateView)


class Index(ListView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            queryset = Aviso.objects.all()
            if self.request.user.tipo_persona is '1':
                context = {'title': 'Lista de avisos',
                           'year': datetime.now().year,
                           'object_list': queryset,
                           'total': range(len(queryset))
                           }
                return render(request, self.template_name, context)

            elif self.request.user.tipo_persona is '2':
                id = self.request.user.id
                docente = Docente.objects.filter(docente_id=id)
                tutor = [b.tutor for b in docente]
                queryset = Aviso.objects.filter(Q(dirigido_a='1') | Q(dirigido_a='2'))
                materias = Materia.objects.raw(
                    'SELECT DISTINCT materia_materia.* FROM usuario_docente '
                    'INNER JOIN materia_materiadocente_docente on materia_materiadocente_docente.docente_id = usuario_docente.id '
                    'INNER JOIN materia_materiadocente_materia on materia_materiadocente_materia.materiadocente_id = materia_materiadocente_docente.materiadocente_id '
                    'INNER JOIN materia_materia on materia_materia.id = materia_materiadocente_materia.materia_id '
                    'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_docente.docente_id '
                    'WHERE usuario_usuario.id = %s ORDER by materia_materia.grado ASC ', [id])
                if tutor == ['1']:
                    print(range(len(queryset)))
                    context = {'title': 'Lista de avisos',
                               'year': datetime.now().year,
                               'materias': materias,
                               'grupotutor': docente,
                               'object_list': queryset,
                               'total': range(len(queryset))
                               }
                    return render(request, self.template_name, context)
                else:
                    context = {'title': 'Lista de avisos',
                               'year': datetime.now().year,
                               'materias': materias,
                               'object_list': queryset,
                               'total': range(len(queryset))
                               }
                    return render(request, self.template_name, context)
            elif self.request.user.tipo_persona is '3':
                padreid = self.request.user.id
                queryset = Aviso.objects.filter(Q(dirigido_a='1') | Q(dirigido_a='3') &
                                                Q(grupo__isnull=True) & Q(grado__isnull=True))
                queryset2 = Aviso.objects.raw(
                    'SELECT DISTINCT dashboard_aviso.* FROM alumno_alumno '
                    'INNER JOIN usuario_padrealumno_alumno ON usuario_padrealumno_alumno.alumno_id=alumno_alumno.matricula '
                    'INNER JOIN usuario_padrealumno_padre ON usuario_padrealumno_padre.padrealumno_id=usuario_padrealumno_alumno.padrealumno_id '
                    'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
                    'INNER JOIN dashboard_aviso on dashboard_aviso.grupo = alumno_alumno.grupo '
                    'INNER JOIN dashboard_aviso as a on a.grado = alumno_alumno.grado '
                    'INNER JOIN usuario_usuario ON usuario_usuario.id=usuario_padrefam.padre_id WHERE usuario_padrefam.padre_id = %s',
                    [padreid])
                num = len(queryset)
                print(num)
                if queryset2:
                    num2 = 0
                    for a in queryset2:
                        print(a)
                        num2 += 1
                    print(num2)
                    context = {'title': 'Lista de avisos',
                               'year': datetime.now().year,
                               'object_list': queryset,
                               'object_list2': queryset2,
                               'total': range(num + num2)
                               }
                else:
                    context = {'title': 'Lista de avisos',
                               'year': datetime.now().year,
                               'object_list': queryset,
                               'total': range(num)
                               }
                return render(request, self.template_name, context)
        else:
            context = {'title': 'Lista de avisos',
                       'year': datetime.now().year,
                       }
            return render(request, self.template_name, context)


class LoginView(FormView):
    template_name = 'dashboard/login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['title'] = 'Inicio de sesion'
        return context

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('dashboard:index'))


def logout_view(request):
        logout(request)
        return HttpResponseRedirect(reverse('dashboard:index'))


def avisos(request):
    return render(request, 'dashboard/avisos.html', {'title': 'Inicio', 'year': datetime.now().year, })


class AvisoCreateView(CreateView):  # Agregar nuevo incidencia
    template_name = 'dashboard/avisos.html'
    form_class = AvisoForm

    def get_context_data(self, **kwargs):
        context = super(AvisoCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['title'] = 'Agregar aviso'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            print("Form valido")
        if form.is_valid():
            print("Formularios validos ")
            incidencia = form.save(commit=False)
            incidencia.save()
            enviar_notificacion(incidencia.id)
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        print(form.cleaned_data)
        enviar_notificacion(self.kwargs.get("pk"))
        return super().form_valid(form)


class AvisoDetailView(DetailView):  # Detalle de un alumno por su id
    template_name = 'dashboard/detalle.html'
    model = Aviso

    def get_context_data(self, queryset=None, *args, **kwargs):
        context = super(AvisoDetailView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = Aviso.objects.filter(id=_id)
        context['object'] = queryset
        context['year'] = datetime.now().year
        context['title'] = 'Detalles del aviso'
        return context


class AvisoUpdateView(UpdateView):  # Mofificar un usuario por su id
    template_name = 'dashboard/actualizar.html'
    model = Aviso
    form_class = AvisoForm

    def get_context_data(self, **kwargs):
        context = super(AvisoUpdateView, self).get_context_data(**kwargs)
        _id = self.kwargs.get("pk")
        queryset = Aviso.objects.filter(id=_id)
        context["object"] = queryset
        context['year'] = datetime.now().year
        context['title'] = 'Detalles del aviso'
        return context


class AlumnoListView(ListView):  # Mostrar todos lo usuarios
    template_name = 'dashboard/lista.html'

    def get_queryset(self):
        queryset = Aviso.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset(),
                   'title': 'Lista de avisos',
                   'year': datetime.now().year,
                   }
        return render(request, self.template_name, context)


def enviar_notificacion(id_aviso):
    aviso = Aviso.objects.filter(id=id_aviso)
    print()
    if aviso[0].dirigido_a == '1':
        device = FCMDevice.objects.all()
        device.send_message(title="Nuevo aviso", body=aviso[0].asunto)
        print(device)
    elif aviso[0].dirigido_a == '2':
        print("Maestros")
    else:
        al = {}
        print(aviso[0].grado, aviso[0].grupo)
        if aviso[0].grupo is None and aviso[0].grado is None:
            padres = Usuario.objects.filter(tipo_persona='3').all()
            device = FCMDevice.objects.filter(user__in=padres)
            device.send_message(title="Nuevo aviso", body=aviso[0].asunto)
            print(device)
        if aviso[0].grupo is not None and aviso[0].grado is None:
            print("grupo")
            padres = Usuario.objects.raw(
                'SELECT DISTINCT usuario_usuario.* FROM alumno_alumno '
                'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
                'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
                'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
                'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
                'INNER JOIN dashboard_aviso on dashboard_aviso.grupo = alumno_alumno.grupo '
                'WHERE dashboard_aviso.id = %s', [id_aviso])
            al['padres'] = [o.id for o in padres]
            num = len(al['padres'])
            for x in range(num):
                device = FCMDevice.objects.filter(user=al['padres'][x])
                print(device)
                device.send_message(title="Nuevo aviso", body=aviso[0].asunto)

        if aviso[0].grupo is None and aviso[0].grado is not None:
            print("grado")
            padres = Usuario.objects.raw(
                'SELECT DISTINCT usuario_usuario.* FROM alumno_alumno '
                'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
                'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
                'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
                'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
                'INNER JOIN dashboard_aviso on dashboard_aviso.grado = alumno_alumno.grado '
                'WHERE dashboard_aviso.id = %s', [id_aviso])
            al['padres'] = [o.id for o in padres]
            num = len(al['padres'])
            for x in range(num):
                device = FCMDevice.objects.filter(user=al['padres'][x])
                print(device)
                device.send_message(title="Nuevo aviso", body=aviso[0].asunto)

        if aviso[0].grupo is not None and aviso[0].grado is not None:
            print("todosssss")
            padres = Usuario.objects.raw(
                'SELECT DISTINCT usuario_usuario.* FROM alumno_alumno '
                'INNER JOIN usuario_padrealumno_alumno on usuario_padrealumno_alumno.alumno_id = alumno_alumno.matricula '
                'INNER JOIN usuario_padrealumno_padre on usuario_padrealumno_padre.padrealumno_id = usuario_padrealumno_alumno.padrealumno_id '
                'INNER JOIN usuario_padrefam ON usuario_padrefam.id=usuario_padrealumno_padre.padrefam_id '
                'INNER JOIN usuario_usuario on usuario_usuario.id = usuario_padrefam.padre_id '
                'INNER JOIN dashboard_aviso on dashboard_aviso.grupo = alumno_alumno.grupo '
                'INNER JOIN dashboard_aviso as a on a.grado = alumno_alumno.grado '
                'WHERE dashboard_aviso.id = %s', [id_aviso])
            al['padres'] = [o.id for o in padres]
            num = len(al['padres'])
            for x in range(num):
                device = FCMDevice.objects.filter(user=al['padres'][x])
                print(device)
                device.send_message(title="Nuevo aviso", body=aviso[0].asunto)
