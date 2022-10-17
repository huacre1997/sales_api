# Importamos la clase models del módulo django.db
from django.db import models

# Importamos las clases MinValueValidator, MaxValueValidator para agregar validaciones al atributo "percent_discount"
from django.core.validators import MinValueValidator, MaxValueValidator

# Importamos la clase Currency de la aplicación Sales
from apps.sales.models import Currency

# Create your models here.

class UnitMeasureCategory(models.Model):
    """
    Clase de Categoría de Unidades de Medida
    Ejemplo: Peso,  Volumen, Longitud
    """
    #Autofield : autoincremental
    id = models.AutoField(primary_key=True,verbose_name="Código")
    name =  models.CharField(max_length=30,verbose_name="Nombre de categoría")
    #auto_now_add : se agrega automáticamente cuando ocurre un nuevo registro
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    #auto_new_add : se agrega automáticamente cuando ocurre se actualiza el registro
    update_at = models.DateTimeField(auto_now=True,verbose_name="Fecha de modificación")

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
        verbose_name = "Categoría de Unidades de Medida"
    

class UnitMeasure(models.Model):
    """
    Clase de Unidad de Medida
    Ejemplo: Kg -> Categoría (Peso), g -> Categoría (Peso), l -> Categoría (Volumen), ml
    """
    id = models.AutoField(primary_key=True,verbose_name="Código")
    name = models.CharField(max_length=30,verbose_name="Nombre") 
    # foreign_key: categoría de unidad de medida
    unit_measure_category_id = models.ForeignKey(UnitMeasureCategory,on_delete=models.CASCADE,default=None,verbose_name="Categoría de Unidad de Medida")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    update_at = models.DateTimeField(auto_now=True,verbose_name="Fecha de modificación")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "unit_measure"
        verbose_name = "Unidades de Medida"


class ProductCategory(models.Model):
    """
    Clase de Categoría del producto
    Ejemplo: Lacteós, Bebidas, Carnes, Pastas
    """
    id = models.AutoField(primary_key=True,verbose_name="Código")
    name = models.CharField(max_length=30,verbose_name="Nombre")
    # PositiveSmallIntegerField : Entero positivo pequeño
    percent_discount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(75)], verbose_name="Descuento (%)")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    update_at = models.DateTimeField(auto_now=True,verbose_name="Fecha de modificación")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ProductCategory, self).save(*args, **kwargs)

    class Meta:
        db_table = "product_category"
        verbose_name = "Categoría de Producto"


class Product(models.Model):
    """
    Clase de Producto
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=5,unique=True,verbose_name="Código")
    name = models.CharField(max_length=60,blank=False,verbose_name="Nombre")

    # foreign_key: categoría de producto
    product_category_id = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,default=None,verbose_name="Categoría Producto")
    # foreign_key: unidad de medida
    unit_measure_id = models.ForeignKey(UnitMeasure,on_delete=models.CASCADE,default=None,verbose_name="Unidad de Medida")
    # foreign_key: divisa
    currency_id = models.ForeignKey(Currency,on_delete=models.CASCADE,default=None,verbose_name="Moneda")
    # precio de venta base
    base_sale_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Precio de Venta Base")
    # require: from django.core.validators
    percent_discount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(75)], verbose_name="Descuento (%)")
    # monto de descuento
    discount_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Monto Descuento")
    # precio de venta
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Precio de Venta")
    # stock: PositiveIntegerField
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    # Activo: BooleanField
    active = models.BooleanField(default=True, verbose_name="Activo")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha Modificación")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Sobre escribimos el método save de la clase Model.
        """
        # Calculamos el monto de descuento
        self.discount_amount = round((int(self.percent_discount)/100)*float(self.base_sale_price),2)
        
        # Calculamos el precio de venta
        self.sale_price = float(self.base_sale_price) - float(abs(self.discount_amount))
        
        # Guardamos información del modelo
        super(Product, self).save(*args, **kwargs)

    class Meta:
        db_table = "product"
        verbose_name = "Producto"