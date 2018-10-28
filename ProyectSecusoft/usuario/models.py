from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
    )
from django.urls import reverse
from alumno.models import Alumno
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, tipo_persona, sexo, telefono, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Email obligatorio")
        if not password:
            raise ValueError("Contraseña obligatoria")
        if not nombre:
            raise ValueError("Nombre obligatorio")
        if not apellido:
            raise ValueError("Apellido obligatorio")
        if not tipo_persona:
            raise ValueError("tipo de usuario obligatorio")
        user_obj = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            tipo_persona=tipo_persona,
            password=password,
            sexo=sexo,
            telefono=telefono,
        )
        user_obj.set_password(password)  # change user password
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, nombre, apellido, tipo_persona, password, sexo, telefono):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            nombre=nombre,
            apellido=apellido,
            tipo_persona=tipo_persona,
            password=password,
            sexo=sexo,
            telefono=telefono,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, tipo_persona, password, sexo, telefono):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            nombre=nombre,
            apellido=apellido,
            tipo_persona=tipo_persona,
            password=password,
            sexo=sexo,
            telefono=telefono,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    usuario_tipo = (
        ('1', 'Administrador'),
        ('2', 'Docente'),
        ('3', 'Padre de familia'),
    )
    sexo_tipo = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    tipo_persona = models.CharField(max_length=2, choices=usuario_tipo)
    sexo = models.CharField(max_length=1, choices=sexo_tipo, default='H')
    telefono = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['nombre', 'apellido', 'tipo_persona', 'sexo', 'telefono']  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def get_absolute_url(self):
        return reverse('usuarios:usuario-detalle', kwargs={'pk': self.id})

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.nombre, self.apellido)

    def get_id(self):
        return self.id

    def get_sex(self):
        return self.sexo

    def get_type_str(self):
        return self.get_tipo_persona_display()

    def get_type(self):
        return self.tipo_persona

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_aactive(self):
        "Is the user active?"
        return self.is_active


class PadreFam(models.Model):
    padre = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s: %s' % (self.padre, self.padre.nombre, self.padre.apellido)

    def get_absolute_url(self):
        return reverse('usuarios:usuario-detalle', kwargs={'pk': self.padre_id})


class PadreAlumno(models.Model):
    padre = models.ManyToManyField(PadreFam)
    alumno = models.ManyToManyField(Alumno)


class Docente(models.Model):
    tutor_tipo = (
        ('1', 'Si'),
        ('2', 'No'),
    )
    grado_tipo = (
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),)
    grupo_tipo = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),)
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tutor = models.CharField(max_length=5, choices=tutor_tipo, default='1')
    grupo = models.CharField(max_length=10, choices=grupo_tipo, null=True, blank=True)
    grado = models.CharField(max_length=10, choices=grado_tipo, null=True, blank=True)

    def __str__(self):
        return '%s %s: %s' % (self.docente, self.docente.nombre, self.docente.apellido)
