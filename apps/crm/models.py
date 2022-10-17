from django.db import models

# Create your models here.
class CategoryCustomer(models.Model):
    """
    Categoria del Cliente.
    Ejemplo: Restaurante, Supermercado
    """
    # Atributo "id_category_customer" => columna "id_category_customer" de la tabla
    # Identificador de registro de nuestra tabla.
    id_category_customer = models.AutoField(primary_key=True, db_column="id_category_customer")

    # Atributo "name" => columna "name" de la tabla
    # Nombre de la Categoría de Cliente
    name = models.CharField(max_length=30, verbose_name="Nombre de la categoria del cliente")

class District(models.Model):
    """
    Distrito.
    Ejemplo: San Juan, Villa Maria
    """
    # Atributo "id_district" => columna "id_district" de la tabla
    # Identificador de registro de nuestra tabla.
    id_district = models.AutoField(primary_key=True, db_column="id_district")

    # Atributo "name" => columna "name" de la tabla
    # Nombre del Distrito
    name = models.CharField(max_length=30, verbose_name="Nombre del Distrito")

class Customer(models.Model):
    """
    Clase de Cliente.
    Ejemplo: Makro SAC, Tottus SAC
    """
    # Atributo "id_customer" => columna "id_customer" de la tabla
    # Identificador de registro de nuestra tabla.
    id_customer = models.AutoField(primary_key=True, db_column="id_customer")

    # Atributo "customer_name" => columna "customer_name" de la tabla
    # Nombre de Categoría de Unidad de Medida
    customer_name = models.CharField(max_length=30, verbose_name="Nombre del cliente")

    # Atributo "ruc" => columna "ruc" de la tabla
    # ruc de la empresa
    ruc = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación")

    # foreign_key: Categoria del cliente
    id_category_customer = models.ForeignKey(CategoryCustomer, on_delete=models.CASCADE,
                                        default=None, db_column="id_category_customer", verbose_name="Categoria del Cliente")

    # foreign_key: Distrito
    id_district = models.ForeignKey(District, on_delete=models.CASCADE,
                                        default=None, db_column="id_district", verbose_name="Distrito")