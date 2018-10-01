from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
    )
# Create your models here.
from django.urls import reverse


class Persona(models.Model):
    persona_tipo = (
        ('1', 'Administrador'),
        ('2', 'Docente'),
        ('3', 'Padre de familia'),
        ('4', 'Alumno'),
    )
    sexo_tipo = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    tipo_persona = models.CharField(max_length=2, choices=persona_tipo, default='4')
    sexo = models.CharField(max_length=1, choices=sexo_tipo, default='H')
    fecha_nacimiento = models.DateField()
    token = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('usuarios:usuario-detalle', kwargs={'pk': self.id})


class Alumno(models.Model):
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
    alumno = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)
    matricula = models.CharField(help_text="Matricula del alumno", max_length=8, primary_key=True, unique=True)
    grado = models.CharField(max_length=10, choices=grado_tipo, default='1')
    grupo = models.CharField(max_length=10, choices=grupo_tipo, default='A')

    def __str__(self):
        return '%s %s: %s %s grado' % (self.alumno.nombre, self.alumno.apellido, self.matricula, self.get_grado_display())

    def get_absolute_url(self):
        return reverse('usuarios:usuario-detalle-alumnos', kwargs={'pk': self.matricula})


class PadreFam(models.Model):
    padre = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s: %s' % (self.padre.nombre, self.padre.apellido, self.padre.usuario)

    def get_absolute_url(self):
        return reverse('usuarios:usuario-detalle', kwargs={'pk': self.padre_id})


class PadreAlumno(models.Model):
    padre = models.ManyToManyField(PadreFam)
    alumno = models.ManyToManyField(Alumno)


class Docente(models.Model):
    tutor_tipo = (
        ('1', 'Si'),
        ('2', 'No'),
        ('3', 'Temporal'),
    )
    docente = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tutor = models.CharField(max_length=5, choices=tutor_tipo, default='1')

    def __str__(self):
        return '%s %s: %s' % (self.docente.nombre, self.docente.apellido, self.docente.usuario)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Email obligatorio")
        if not password:
            raise ValueError("Contraseña obligatoria")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)  # change user password
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    usuario = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.usuario.nombre

    def get_type_str(self):
        return self.usuario.get_tipo_persona_display()

    def get_type(self):
        return self.usuario.tipo_persona

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
    def is_active(self):
        "Is the user active?"
        return self.active