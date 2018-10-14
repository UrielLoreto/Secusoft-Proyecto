from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


app_name = 'dashboard'
urlpatterns = (
    path('', index, name='index'),
    path('anuncios', avisos, name='avisos'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset-password/', auth_views.password_reset, {
        'template_name': 'registration/password_reset_form.html',
        'post_reset_redirect': 'done/'
    }, name='password_reset'),
    path('reset-password/done/', auth_views.password_reset_done, {
        'template_name': 'registration/password_reset_done.html',
    }, name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', auth_views.password_reset_confirm, {
        'template_name': 'registration/password_reset_confirm.html',
        'post_reset_redirect': 'dashboard:login'
    }, name='password_reset_confirm'),
)
