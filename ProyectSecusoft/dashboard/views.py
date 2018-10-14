from django.shortcuts import render
from datetime import datetime
from django.contrib.auth import logout
from django.urls import reverse

from .forms import LoginForm
from django.http import HttpResponseRedirect
from django.views.generic import (
    FormView
)


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