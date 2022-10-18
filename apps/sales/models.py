from django.db import models

# Importamos la clase District,Customer de la app warehouse
from apps.crm.models import District, Customer
from apps.warehouse.models import Product
from utils.models import ModelBase


class Delivery(ModelBase):
    """
    Categoria del Cliente.
    Ejemplo: Restaurante, Supermercado
    """
    # Atributo "address" => columna "address" de la tabla
    # Nombre de la Categoría de Cliente
    address = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Dirección")

    # Atributo "date" => columna "date" de la tabla
    # Fecha de entrega
    date = models.DateField(blank=False, null=False,
                            verbose_name="Fecha de entrega")

    # foreign_key: Distrito
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 default=None, verbose_name="Distrito")

    # Atributo "status" => columna "status" de la tabla
    # Estado de la entrega
    # Activo: BooleanField
    status = models.BooleanField(
        default=True, verbose_name="Estado de entrega")

    def __str__(self):
        """
        Método para devolver un string que represente al objeto
        """
        return self.address

    class Meta:
        """
        Clase Meta:
        Clase de Django para agregar opciones adicionales a nuestro modelo.
        Link: https://docs.djangoproject.com/en/4.1/ref/models/options/
        """

        # Nombre que recibirá nuestro modelo en la base de datos.
        db_table = "delivery"

        # Texto que aparecerá en nuestra aplicación.
        verbose_name = "Entrega"

        # Texto que aparecerá en nuestra aplicación en plural.
        verbose_name_plural = "Entregas"


class Order(ModelBase):
    """
    Pedido.
    Ejemplo: 202200001
    """
    # Atributo "number_order" => columna "number_order" de la tabla
    # Numero del pedido
    code = models.CharField(
        max_length=9, unique=True, null=False, blank=False, verbose_name="Número del Pedido")

    # foreign_key: Cliente
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 default=None, verbose_name="Cliente")

    # foreign_key: Entrega
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE,
                                 default=None, verbose_name="Entrega")

    # Atributo "status" => columna "status" de la tabla
    # Estado del pedido
    # Activo: BooleanField
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "order"
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class OrderDetail(ModelBase):
    """
    Detalle del Pedido.
    Ejemplo: boletas o facturas con los productos
    """
    # foreign_key: Orden
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              default=None, verbose_name="Pedido")

    # foreign_key: Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                default=None, verbose_name="Producto")

    # Atributo "quantity" => columna "quantity" de la tabla
    # Cantidad de detalle del pedido
    quantity = models.PositiveIntegerField(
        default=0, null=False, blank=False, verbose_name="Cantidad")

    # Atributo "discount_amount" => columna "discount_amount" de la tabla
    # Monto de Descuento
    discount_amount = models.DecimalField(
        max_digits=7, decimal_places=2, default=0, verbose_name="Monto de Descuento")

    # Atributo "subtotal" => columna "subtotal" de la tabla
    # Subtotal
    subtotal = models.DecimalField(
        max_digits=7, decimal_places=2, default=0, verbose_name="Subtotal")

    def __str__(self):
        return self.order.code

    class Meta:
        db_table = "order_detail"
        verbose_name = "Detalle del Pedido"
        verbose_name_plural = "Detalles del Pedido"

    def save(self, *args, **kwargs):
        """
        Sobre escribimos el método save de la clase Model.
        """
        if (int(self.product.product_category.percent_discount) > int(self.product.percent_discount)):
            # Calculamos el monto de descuento
            self.discount_amount = round(
                (int(self.product.product_category.percent_discount) / 100) * float(self.product.base_sale_price), 2)

            # Calculamos el precio de venta del producto
            self.product.sale_price = float(self.product.base_sale_price) - \
                float(abs(self.discount_amount))

        if (int(self.product.percent_discount) > int(self.product.product_category.percent_discount)):
            # Calculamos el monto de descuento
            self.discount_amount = round(
                (int(self.product.percent_discount) / 100) * float(self.product.base_sale_price), 2)

            # Calculamos el precio de venta del producto
            self.product.sale_price = float(self.product.base_sale_price) - \
                float(abs(self.discount_amount))

        # Verificamos la cantidad del stock
        if (self.product.stock > 0 and self.quantity <= self.product.stock):
            # Descontamos la cantidad del stock
            self.product.stock = self.product.stock - self.quantity

        # Guardamos información del modelo
        super(OrderDetail, self).save(*args, **kwargs)
