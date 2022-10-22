from dataclasses import field
from rest_framework.serializers import ModelSerializer
from apps.sales.models import Delivery, Order, OrderDetail
from rest_framework import serializers
from apps.crm.api.serializers import CustomerSerializer
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
    total_igv = serializers.FloatField()
    total = serializers.FloatField()

    class Meta:
        model = Order
        fields = ["id", "code", "date", "code",
                  "total_discount", "total_subtotal", "total_igv", "total"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

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
        if not product.is_active:
            raise serializers.ValidationError(
                f'El producto {product.name} no se encuentra activo')
        return data


class OrderSearchSerializer(ModelSerializer):
    """
    Clase para convertir un objeto Order a un formato JSON.
    """
    details = OrderDetailSerializer(
        many=True, source='orderdetail_set')

    class Meta:
        model = Order
        fields = ["id", "code", "date", "details"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["customer"] = CustomerSerializer(instance.customer).data
        data["delivery"] = DeliverySerializer(instance.delivery).data
        data["total"] = sum([float(i["subtotal"]) for i in data["details"]])
        data["total_discount"] = sum([float(i["discount_amount"]) for i in data["details"]])
        return data


class OrderCustomer(ModelSerializer):
    """
    Clase para convertir un objeto Order a un formato JSON.
    """
    details = OrderDetailSerializer(
        many=True, read_only=True, source='orderdetail_set')

    class Meta:
        model = Order
        fields = ["id", "code", "date", "code", "details"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["customer"] = instance.customer.company_name
        data["date_delivery"] = instance.delivery.date
        return data
