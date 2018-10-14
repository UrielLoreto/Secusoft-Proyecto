from django.contrib import admin
from usuario.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Usuario
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_active')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informacion personal', {'fields': ()}),
        ('Permisos', {'fields': ('admin', 'is_active', 'staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Register your models here.

admin.site.register(Persona)
admin.site.register(PadreAlumno)
admin.site.register(PadreFam)
admin.site.register(Alumno)

admin.site.register(Docente)
admin.site.register(Usuario, UserAdmin)

admin.site.unregister(Group)
