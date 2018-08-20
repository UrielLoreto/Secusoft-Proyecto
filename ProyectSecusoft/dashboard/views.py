from django.shortcuts import render
from datetime import datetime


def index(request):
    return render(request, 'dashboard/index.html', {'title': 'Inicio', 'year': datetime.now().year, })


def login(request):
    return render(request, 'dashboard/login.html', {'title': 'Inicio de Sesion', 'year': datetime.now().year, })