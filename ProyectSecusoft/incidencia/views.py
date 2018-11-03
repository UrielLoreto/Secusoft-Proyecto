from datetime import datetime
from django.shortcuts import redirect, get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from incidencia.serializers import *
from usuario.models import PadreFam, PadreAlumno
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
            incidencia = form.save(commit=False)
            incidenciaalumnos = form2.save(commit=False)
            incidencia.save()
            incidenciaalumnos.save()
            incidenciaalumnos.alumno.add(request.POST['alumno'])
            incidenciaalumnos.incidencia.add(incidencia)
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class IncidenciaTipoCreateView(CreateView):  # Agregar nuevo incidencia
    template_name = 'incidencia/incidencia_agregar.html'
    form_class = IncidenciaTipoForm

    def get_context_data(self, **kwargs):
        context = super(IncidenciaTipoCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        context['year'] = datetime.now().year
        context['title'] = 'Agregar incidencia'
        context['incidencias'] = TipoIndicencia.objects.all()
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
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


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
        context = {'object_list': self.get_queryset(),
                   'title': 'Lista de incidencias',
                   'year': datetime.now().year,
                   'Tipo': 'true',
                   }
        return render(request, self.template_name, context)


class IncidenciaDetailView(DetailView):  # Detalle de un incidencia por su id
    model = Incidencia
    template_name = 'incidencia/incidencia_detalle.html'

    def get_context_data(self, queryset=None, *args, **kwargs):
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
            'Select alumno_alumno.matricula, incidencia_incidencia.id_incidencia '
            'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
            'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
            'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
            'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
            'WHERE incidencia_incidencia.id_incidencia =%s ', [_id])
        print(_id)
        # queryset2 = Cita.objects.filter(matricula__in=[o.matricula for o in self.get_queryset()])
        context["object"] = queryset
        context["alumnos"] = queryset2
        context['year'] = datetime.now().year
        context['title'] = 'Detalles de incidencia'
        return context


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
                                              'LEFT JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_incidencia.citaincidencia_id '
                                              'WHERE usuario_padrefam.padre_id =%s', [padreid])

        else:
            queryset = Incidencia.objects.raw('Select cita_cita.id_cita, alumno_alumno.matricula, alumno_alumno.grado, alumno_alumno.grupo, incidencia_incidencia.*, incidencia_tipoindicencia.* '
                                              'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
                                              'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
                                              'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
                                              'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
                                              'LEFT JOIN cita_citaincidencia_incidencia on cita_citaincidencia_incidencia.incidencia_id = incidencia_incidencia.id_incidencia '
                                              'LEFT JOIN cita_cita ON cita_cita.id_cita = cita_citaincidencia_incidencia.citaincidencia_id')
        return queryset

    def get(self, request, *args, **kwargs):
        if self.request.user.tipo_persona is '3':
            context = {'object_list': self.get_queryset(),
                       'title': 'Lista de incidencias',
                       'padre': True,
                       'year': datetime.now().year,
                       'alumno': 'true',
                       }
        else:
            context = {'object_list': self.get_queryset(),
                       'title': 'Lista de incidencias',
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
            'year': datetime.now().year,
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.tipo_persona is '3':
            queryset = PadreAlumno.objects.filter(padre__padre_id=user.pk)
            alumnos = {}
            for a in queryset:
                alumnos = a.alumno.values('matricula'), a.alumno.values('nombre'), a.alumno.values('grado'), a.alumno.values('grupo')
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'alumnos': alumnos,
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

    def post(self, request, *args, **kwargs):
        user = self.kwargs.get("pk")
        incidencia = []
        incidencias = {}
        aaa = []
        incidencia2 ={}
        bbb = []
        queryset = Incidencia.objects.raw(
            'Select alumno_alumno.matricula, alumno_alumno.grado, alumno_alumno.grupo, incidencia_incidencia.*, incidencia_tipoindicencia.* '
            'FROM alumno_alumno INNER JOIN incidencia_incidenciaalumno_alumno on incidencia_incidenciaalumno_alumno.alumno_id = alumno_alumno.matricula '
            'INNER JOIN incidencia_incidenciaalumno_incidencia ON incidencia_incidenciaalumno_incidencia.incidenciaalumno_id=incidencia_incidenciaalumno_alumno.incidenciaalumno_id '
            'INNER JOIN incidencia_incidencia ON incidencia_incidencia.id_incidencia = incidencia_incidenciaalumno_incidencia.incidencia_id '
            'INNER JOIN incidencia_tipoindicencia ON incidencia_tipoindicencia.id_tipo = incidencia_incidencia.incidencia_id '
            'WHERE alumno_alumno.matricula=%s', [user])
        for a in queryset:
            incidencia.append((a.asunto, a.incidencia_id, a.estatus, a.fecha_incidencia.date(), a.observaciones))
        if len(incidencia) != 0:
            b = 0
            for a in incidencia:
                incidencias['id'] = a[1]
                incidencias['estatus'] = a[2]
                incidencias['fecha_incidencia'] = a[3]
                incidencias['asunto'] = a[0]
                incidencias['observaciones'] = a[4]
                aaa = incidencias
                for hola, hose in aaa.items():
                    # print(hola, hose)
                    bbb.append({hola: hose})
                incidencia2[b] = list(bbb)
                bbb.clear()
                aaa.clear()
                # print(aaa)
                b += 1
            # print(incidencia2)
            return Response({
                'incidencia': incidencia2,
            })
        else:
            return Response({
                'incidencia': 'ninguna',
            })


class TipoIncidenciaView(viewsets.ModelViewSet):
    queryset = TipoIndicencia.objects.all()
    serializer_class = TipoIncidenciaSerializer


class IncidenciaDetailViewCel(APIView):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['matricula']

        queryset = Alumno.objects.filter(matricula=user)
        return Response({
            'token': queryset.nombre,
            'user_id': queryset.grado,
        })