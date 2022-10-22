from rest_framework.serializers import ModelSerializer
from apps.crm.models import CustomerCategory, District, Customer
from utils.constants import IGV
from utils.base.serializers import BaseSerializer


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


class CustomerOrdersSerializer(ModelSerializer):
    """
    Clase para convertir un objeto Order a un formato JSON.
    """
    from apps.sales.api.serializers import OrderSearchSerializer

    orders = OrderSearchSerializer(
        many=True, read_only=True, source='order_set')

    class Meta:
        model = Customer
        fields = ["id", "company_name", "orders"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["customer_category"] = CustomerCategorySerializer(
            instance.customer_category).data
        # data["sub_total"] = sum(
        #     [i["sub_total"] for i in data["orders"]])
        # data["igv"] = data["sub_total"] * IGV / 100
        # data["total"] = data["igv"] + data["sub_total"]
        return data
