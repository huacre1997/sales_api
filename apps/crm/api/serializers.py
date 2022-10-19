from rest_framework.serializers import ModelSerializer
from apps.crm.models import CustomerCategory,District

class CustomerCategorySerializer(ModelSerializer):
    """
    Clase para convertir un objeto CustomerCategory a un formato JSON.
    """
    class Meta:
        model = CustomerCategory
        #fields = ['code','name']
        fields = '__all__'

class DistrictSerializer(ModelSerializer):
    """
    Clase para convertir un objeto District a un formato JSON.
    """
    class Meta:
        model = District
        #fields = ['code','name']
        fields = '__all__'