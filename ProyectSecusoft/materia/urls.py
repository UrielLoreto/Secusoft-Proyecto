from django.urls import path
from .views import *
app_name = 'materias'
urlpatterns = [
    path('', MateriaListView.as_view(), name='materia-lista'),
    path('agregar/', MateriaListView.as_view(), name='materia-nueva'),
]
