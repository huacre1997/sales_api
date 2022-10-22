from rest_framework import serializers
from apps.warehouse.models import ProductCategory, Product
from utils.serializers import BaseSerializer


class ProductCategorySerializer(BaseSerializer):
    """
    Clase para convertir un objeto ProductCategory a un formato JSON.
    """
    name = serializers.CharField(required=False, max_length=100)

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'percent_discount']


class ProductSerializer(BaseSerializer):
    """
    Clase para convertir un objeto ProductCategory a un formato JSON.
    """

    class Meta:
        model = Product
        exclude = ['created_by', 'created_at', 'is_active']
