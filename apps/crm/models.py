from django.db import models
from utils.base.models import ModelBase


class CustomerCategory(ModelBase):
    """
    Categoria del Cliente.
    Ejemplo: Restaurante, Supermercado
    """
    # Atributo "name" => columna "name" de la tabla
    # Nombre de la Categoría de Cliente
    name = models.CharField(
        max_length=30, verbose_name="Nombre de la categoría del cliente")

    def __str__(self):
        """
        Método para devolver un string que represente al objeto
        """
        return self.name

    class Meta:
        """
        Clase Meta:
        Clase de Django para agregar opciones adicionales a nuestro modelo.
        Link: https://docs.djangoproject.com/en/4.1/ref/models/options/
        """
        # Nombre que recibirá nuestro modelo en la base de datos.
        db_table = "customer_category"

        # Texto que aparecerá en nuestra aplicación.
        verbose_name = "Categoria del cliente"

        # Texto que aparecerá en nuestra aplicación en plural.
        verbose_name_plural = "Categorías del cliente"

        ordering = ["-id"]


class District(ModelBase):
    """
    Distrito.
    Ejemplo: San Juan, Villa Maria
    """
    # Atributo "name" => columna "name" de la tabla
    # Nombre del Distrito
    name = models.CharField(max_length=40, verbose_name="Nombre del Distrito")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "district"
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"


class Customer(ModelBase):
    """
    Clase de Cliente.
    Ejemplo: Makro SAC, Tottus SAC
    """
    # Atributo "customer_name" => columna "customer_name" de la tabla
    company_name = models.CharField(
        max_length=100, null=False,
        blank=False, verbose_name="Razón social")

    # Atributo "ruc" => columna "ruc" de la tabla
    # ruc de la empresa
    ruc = models.CharField(max_length=11, null=False,
                           blank=False, unique=True, verbose_name="RUC")

    # foreign_key: Categoria del cliente
    customer_category = models.ForeignKey(CustomerCategory, on_delete=models.CASCADE,
                                          default=None, verbose_name="Categoria del Cliente")

    # foreign_key: Distrito
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 default=None, verbose_name="Distrito")

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "customer"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["-id"]
