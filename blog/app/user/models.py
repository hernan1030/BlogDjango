
# para creacion de modelos
from django.db import models

# importaciones para traer el el usuario y manipular sus campos
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# extraer el managers
from .managers import UserManagers


# Crear modelo aqui
class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField('Nombres', max_length=100)
    ocupation = models.CharField('Ocupacion', max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_birth = models.DateField('Fecha de nacimiento', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    verificationcode = models.CharField(max_length=6, blank=True)

    objects = UserManagers()

    # Utiliza el campo "email" como el identificador único de usuario
    USERNAME_FIELD = 'email'

    # este capo como no lo tengo como blank true , lo debo poner aqui para que sea solicitado
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name
