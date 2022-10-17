from django.db import models

# Importamos la clase District,Customer de la app warehouse
from apps.crm.models import District,Customer
from apps.warehouse.models import Product

# Importamos las clases MinValueValidator, MaxValueValidator para agregar validaciones
# al atributo "percent_discount"
# Link: https://docs.djangoproject.com/en/4.1/ref/validators/#module-django.core.validators
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Currency(models.Model):
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
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3,unique=True, verbose_name="Código")
    symbol = models.CharField(max_length=4, verbose_name="Simbolo")
    name = models.CharField(max_length=20, verbose_name="Nombre")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Moficación")

    def __str__(self):
        return f"{self.symbol} {self.code}"

    class Meta:
        db_table = "currency"
        verbose_name = "Moneda"

class Delivery(models.Model):
    """
    Categoria del Cliente.
    Ejemplo: Restaurante, Supermercado
    """
    # Atributo "id_delivery" => columna "id_delivery" de la tabla
    # Identificador de registro de nuestra tabla.
    id_delivery = models.AutoField(primary_key=True, db_column="id_delivery")

    # Atributo "address" => columna "address" de la tabla
    # Nombre de la Categoría de Cliente
    address = models.CharField(max_length=30, verbose_name="Direccion")

    # Atributo "date" => columna "date" de la tabla
    # Fecha de entrega
    date = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha Creación")

    # foreign_key: Distrito
    id_district = models.ForeignKey(District, on_delete=models.CASCADE,
                                        default=None, db_column="id_district", verbose_name="Distrito")

    # Atributo "status" => columna "status" de la tabla
    # Estado de la entregaç
    # Activo: BooleanField
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return self.address

    class Meta:
        db_table = "delivery"
        verbose_name = "Entrega"

class Order(models.Model):
    """
    Pedido.
    Ejemplo: 202200001
    """
    # Atributo "id_delivery" => columna "id_delivery" de la tabla
    # Identificador de registro de nuestra tabla.
    id_order = models.AutoField(primary_key=True, db_column="id_order")
    
    # Atributo "number_order" => columna "number_order" de la tabla
    # Numero del pedido
    number_order = models.CharField(max_length=30, verbose_name="Numero del Pedido")

    # foreign_key: Cliente
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                        default=None, db_column="id_customer", verbose_name="Cliente")

    # foreign_key: Entrega
    id_delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE,
                                        default=None, db_column="id_delivery", verbose_name="Entrega")

    # Atributo "status" => columna "status" de la tabla
    # Estado del pedido
    # Activo: BooleanField                                    
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return self.number_order

    class Meta:
        db_table = "order"
        verbose_name = "Pedido"

class OrderDetail(models.Model):
    """
    Detalle del Pedido.
    Ejemplo: boletas o facturas con los productos
    """
    # foreign_key: Pedido
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE,
                                        default=None, db_column="id_order", verbose_name="Pedidp")

    # foreign_key: Producto
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                        default=None, db_column="id", verbose_name="Producto")

    # Atributo "quantity" => columna "quantity" de la tabla
    # Cantidad de detalle del pedido
    quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad")

    # require: from django.core.validators
    percent_discount = models.PositiveSmallIntegerField(default=0, validators=[
                                                        MinValueValidator(0), MaxValueValidator(60)], verbose_name="Descuento (%)")

    # Atributo "discount_amount" => columna "discount_amount" de la tabla
    # Monto de Descuento
    discount_amount = models.DecimalField(
        max_digits=7, decimal_places=2, default=0, verbose_name="Monto de Descuento")

    # Atributo "subtotal" => columna "subtotal" de la tabla
    # Subtotal
    subtotal = models.DecimalField(
        max_digits=7, decimal_places=2, default=0, verbose_name="Subtotal")

    def __str__(self):
        return self.subtotal

    class Meta:
        db_table = "order_detail"
        verbose_name = "Detalle del Pedido"

    def save(self, *args, **kwargs):
        """
        Sobre escribimos el método save de la clase Model.
        """
        if(int(self.id_product.product_category_id.percent_discount) > int(self.id_product.percent_discount)):
            # Calculamos el monto de descuento
            self.discount_amount = round(
            (int(self.id_product.product_category_id.percent_discount)/100)*float(self.id_product.base_sale_price), 2)
        
            # Calculamos el precio de venta del producto
            self.id_product.sale_price = float(self.id_product.base_sale_price) - \
                float(abs(self.discount_amount))

        if(int(self.id_product.percent_discount) > int(self.id_product.product_category_id.percent_discount)):
            # Calculamos el monto de descuento
            self.discount_amount = round(
            (int(self.id_product.percent_discount)/100)*float(self.id_product.base_sale_price), 2)
        
            # Calculamos el precio de venta del producto
            self.id_product.sale_price = float(self.id_product.base_sale_price) - \
                float(abs(self.discount_amount))
        
        # Guardamos información del modelo
        super(OrderDetail, self).save(*args, **kwargs)