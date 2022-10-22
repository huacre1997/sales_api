from django.db import models
from django.conf import settings


class ModelBase(models.Model):
    """
    Clase modelo base que heredará a todos los modelos de nuestras apps y en consecuencia colocará todos estos campos en cada clase hija
    """
    # Eliminación lógica
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    # auto_now_add : se agrega automáticamente cuando ocurre un nuevo registro
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Fecha de creación")
    # auto_new_add : se agrega automáticamente cuando ocurre se actualiza el registro
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="Fecha de modificación")
    # Almacena el usuario creador
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', null=True, blank=True,
                                   on_delete=models.SET_NULL, verbose_name="Creado por")
    # Almacena el usuario que modifica el registro
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', null=True, blank=True,
                                   on_delete=models.SET_NULL, verbose_name="Modificado por")

    class Meta:
        # Propiedad que indica que será una clase modelo para otros modelos
        abstract = True
