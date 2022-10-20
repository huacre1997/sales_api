from rest_framework.serializers import ModelSerializer
from apps.sales.models import Delivery,Order,OrderDetail

class DeliverySerializer(ModelSerializer):
    """
    Clase para convertir un objeto Delivery a un formato JSON.
    """
    class Meta:
        model = Delivery
        #fields = ['code','name']
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    """
    Clase para convertir un objeto Order a un formato JSON.
    """
    class Meta:
        model = Order
        #fields = ['code','name']
        fields = '__all__'

class OrderDetailSerializer(ModelSerializer):
    """
    Clase para convertir un objeto OrderDetail a un formato JSON.
    """
    class Meta:
        model = OrderDetail
        #fields = ['code','name']
        fields = '__all__'