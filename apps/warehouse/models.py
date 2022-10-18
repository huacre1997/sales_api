# Importamos la clase models del módulo django.db
from django.db import models

# Importamos las clases MinValueValidator, MaxValueValidator para agregar validaciones al atributo "percent_discount"
from django.core.validators import MinValueValidator, MaxValueValidator

from utils.models import ModelBase

# Create your models here.


class Currency(ModelBase):
    """
    Clase Moneda.
    Ejemplo 1: Moneda Sol
    Código: PEN
    Simbolo: S/.
    Nombre: Sol Peruano
    Ejemplo 2: Moneda Dólares Americanos.
    Código: USD
    Simbolo: $.
    Nombre: Dólares Americanos
    """
    code = models.CharField(max_length=3, unique=True, verbose_name="Código")
    symbol = models.CharField(max_length=4, verbose_name="Simbolo")
    name = models.CharField(max_length=20, verbose_name="Nombre")

    def __str__(self):
        return f"{self.symbol} {self.code}"

    class Meta:
        db_table = "currency"
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"


class UnitMeasureCategory(ModelBase):
    """
    Clase de Categoría de Unidades de Medida
    Ejemplo: Peso,  Volumen, Longitud
    """
    name = models.CharField(max_length=30, verbose_name="Nombre de categoría")

    def __str__(self) -> str:
        """
        Método para devolver un string que represente al objeto
        """
        return self.name

    class Meta:
        """
        Clase Meta:
        Clase de Django para agregar opciones adicionales a nuestro modelo.
        """
        # Nombre que recibirá nuestro modelo en la base de datos.
        db_table = "unit_measure_category"
        # Texto que aparecerá en nuestra aplicación.
        verbose_name = "Categoría de Unidad de Medida"

        # Texto que aparecerá en nuestra aplicación en plural.

        verbose_name_plural = "Categorías de Unidad de Medida"


class UnitMeasure(ModelBase):
    """
    Clase de Unidad de Medida
    Ejemplo: Kg -> Categoría (Peso), g -> Categoría (Peso), l -> Categoría (Volumen), ml
    """
    name = models.CharField(max_length=30, verbose_name="Nombre")
    # foreign_key: categoría de unidad de medida
    unit_measure_category = models.ForeignKey(
        UnitMeasureCategory, on_delete=models.CASCADE, default=None, verbose_name="Categoría de Unidad de Medida")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "unit_measure"
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de medida"


class ProductCategory(ModelBase):
    """
    Clase de Categoría del producto
    Ejemplo: Lacteós, Bebidas, Carnes, Pastas
    """
    name = models.CharField(max_length=30, verbose_name="Nombre")
    # PositiveSmallIntegerField : Entero positivo pequeño
    percent_discount = models.PositiveSmallIntegerField(default=0, validators=[
                                                        MinValueValidator(0), MaxValueValidator(75)], verbose_name="Descuento (%)")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_category"
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Producto"


class Product(ModelBase):
    """
    Clase de Producto
    """
    code = models.CharField(max_length=5, unique=True, verbose_name="Código")
    name = models.CharField(max_length=60, blank=False, verbose_name="Nombre")

    # foreign_key: categoría de producto
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, default=None, verbose_name="Categoría Producto")
    # foreign_key: unidad de medida
    unit_measure = models.ForeignKey(
        UnitMeasure, on_delete=models.CASCADE, default=None, verbose_name="Unidad de Medida")
    # foreign_key: divisa
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, default=None, verbose_name="Moneda")
    # precio de venta base
    base_sale_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0, verbose_name="Precio de Venta Base")
    # require: from django.core.validators
    percent_discount = models.PositiveSmallIntegerField(default=0, validators=[
                                                        MinValueValidator(0), MaxValueValidator(75)], verbose_name="Descuento (%)")
    # monto de descuento
    discount_amount = models.DecimalField(
        max_digits=7, decimal_places=2, default=0, verbose_name="Monto Descuento")
    # precio de venta
    sale_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0, verbose_name="Precio de Venta")
    # stock: PositiveIntegerField
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Sobre escribimos el método save de la clase Model.
        """
        # Calculamos el monto de descuento
        self.discount_amount = round(
            (int(self.percent_discount) / 100) * float(self.base_sale_price), 2)

        # Calculamos el precio de venta
        self.sale_price = float(self.base_sale_price) - \
            float(abs(self.discount_amount))

        # Guardamos información del modelo
        super(Product, self).save(*args, **kwargs)

    class Meta:
        db_table = "product"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
