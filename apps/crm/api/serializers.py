from rest_framework.serializers import ModelSerializer
from apps.crm.models import CustomerCategory, District, Customer
from utils.serializers import BaseSerializer


class CustomerCategorySerializer(BaseSerializer):
    """
    Clase para convertir un objeto CustomerCategory a un formato JSON.
    """
    class Meta:
        model = CustomerCategory
        fields = ['id', 'name']


class DistrictSerializer(BaseSerializer):
    """
    Clase para convertir un objeto District a un formato JSON.
    """
    class Meta:
        model = District
        fields = ['id', "name"]


class CustomerSerializer(BaseSerializer):
    """
    Clase para convertir un objeto District a un formato JSON.
    """
    class Meta:
        model = Customer
        fields = ["id", "company_name", "ruc", "customer_category", "district"]
        # Definimos campos obligatorios
        extra_kwargs = {'customer_category': {
            'required': True}, 'district': {'required': True}}

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret["district"] = obj.district.name
        ret["customer_category"] = obj.customer_category.name
        return ret
