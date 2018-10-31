from django.shortcuts import render
from datetime import datetime
from django.contrib.auth import logout
from django.urls import reverse

from dashboard.models import Aviso
from .forms import LoginForm, AvisoForm
from django.http import HttpResponseRedirect
from django.views.generic import (
    FormView, DetailView,
    CreateView, ListView, UpdateView)


def index(request):
    return render(request, 'dashboard/index.html', {'title': 'Inicio', 'year': datetime.now().year, })


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
            return HttpResponseRedirect('..')
        else:
            print(form.data)
            return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        print(form.cleaned_data)
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
