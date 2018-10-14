from django.urls import path
from .views import *

app_name = 'dashboard'
urlpatterns = (
    path('', index, name='index'),
    path('anuncios', avisos, name='avisos'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
)
