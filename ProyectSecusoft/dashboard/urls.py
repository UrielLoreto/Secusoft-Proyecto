from django.urls import path
from . import views
from django.contrib.auth.views import login
app_name = 'dashboard'
urlpatterns = (
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
)
