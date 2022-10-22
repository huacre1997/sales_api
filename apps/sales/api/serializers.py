from dataclasses import field
from rest_framework.serializers import ModelSerializer
from apps.sales.models import Delivery, Order, OrderDetail
from rest_framework import serializers

from apps.warehouse.models import Product


class DeliverySerializer(ModelSerializer):
    """
    Clase para convertir un objeto Delivery a un formato JSON.
    """
    class Meta:
        model = Delivery
        fields = ['address', 'date', "id", "district"]
        # fields = '__all__'


class OrderSerializer(ModelSerializer):
    """
    Clase para convertir un objeto Order a un formato JSON.
    """
    total_subtotal = serializers.FloatField()
    total_discount = serializers.FloatField()

    class Meta:
        model = Order
        fields = ["id", "code", "date", "code",
                  "total_discount", "total_subtotal"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.total_subtotal:
            data["igv"] = instance.total_subtotal * 18 / 100
            data["total"] = data["igv"] + instance.total_subtotal
        else:
            data["igv"] = 0
            data["total"] = 0
        data["customer"] = instance.customer.company_name
        data["date_delivery"] = instance.delivery.date
        return data


class OrderDetailSerializer(ModelSerializer):
    """
    Clase para convertir un objeto OrderDetail a un formato JSON.
    """
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity', 'order',
                  "discount_amount", "subtotal"]

    def validate(self, data):
        quantity = data["quantity"]
        product = data["product"]
        if product.stock < quantity:
            raise serializers.ValidationError(
                f'El stock es insuficiente para el producto {product.name}')
        return data
