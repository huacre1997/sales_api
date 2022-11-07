from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Manager donde se configura que el email será el nuevo medio de autenticación
    """

    def create_user(self, email, password, **extra_fields):
        """
        Crea y guarda el usuario con el email y pass brindado
        """
        if not email:
            raise ValueError(_('El email es requerido'))
        # Validamos que sea un email correcto
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # Hashea su password
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Método que guarda el superuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('EL superuser debe ser : is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('El superuser debe ser: is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('Email'), unique=True)
    country = models.CharField(
        max_length=70, null=False, blank=False, verbose_name=_('País'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
