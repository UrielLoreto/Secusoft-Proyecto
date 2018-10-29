from django.urls import path
from django.views.generic import RedirectView

from .views import *
app_name = 'materias'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard:index')),
    path('lista', MateriaListView.as_view(), name='materia-lista'),
    path('agregar/', MateriaCreateView.as_view(), name='materia-nueva'),
]
