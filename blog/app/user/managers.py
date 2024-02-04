# importamos para crear modelos
from django.db import models

# creacion de manager para usuarios personalizados
from django.contrib.auth.models import BaseUserManager


class UserManagers(BaseUserManager):

    def base_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):

        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self.base_user(email, password, False, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self.base_user(email, password, True, True, True, **extra_fields)

    def codigo_validacio(self, id_user, cod_registro):
        filtrar = self.filter(
            id=id_user, verificationcode=cod_registro).exists()

        return filtrar
