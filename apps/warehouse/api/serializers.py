from rest_framework import serializers
from apps.warehouse.models import ProductCategory
from utils.serializers import BaseSerializer


class ProductCategorySerializer(BaseSerializer):
    """
    Clase para convertir un objeto ProductCategory a un formato JSON.
    """
    name = serializers.CharField(required=False, max_length=100)

    class Meta:
        model = ProductCategory
        fields = ['name', 'percent_discount']
