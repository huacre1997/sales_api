from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.sales.models import OrderDetail
from apps.warehouse.models import Product


@receiver(post_save, sender=OrderDetail)
def update_stock(sender, **kwargs):
    instance = kwargs["instance"]
    product = instance.product
    product.stock -= instance.quantity
    product.save()
