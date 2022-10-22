from asyncio.windows_events import NULL
from venv import create
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from apps.sales.models import Delivery,Order,OrderDetail
from apps.sales.api.serializers import DeliverySerializer,OrderSerializer,OrderDetailSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from utils.viewsets import BaseViewSet

import datetime

class DeliveryViewSet(BaseViewSet):
    """
    Clase ViewSet de Delivery
    """

    # Obtenemos los datos que queremos devolver.
    queryset = Delivery.objects.all()

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = DeliverySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['address']

    search_fields = ['address']

    ordering_fields = ['id']

    @action(detail=True, methods=['put'], name='Eliminar entrega de producto')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False de la entrega de producto
        """
        self.instance = self.get_object()
        if self.instance.is_active:
            super().desactivate(request)
            return Response({"message": "Entrega de producto eliminada"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No existe esa Entrega de Producto"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar Entrega')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True de la Entrega de Producto
        """
        self.instance = self.get_object()
        if not self.instance.is_active:
            super().restore(request)
            return Response({"message": "Entrega de Producto restaurada"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Esa Entrega de Producto ya se encuentra activa"}, status=status.HTTP_200_OK)

class OrderViewSet(BaseViewSet):
    """
    Clase ViewSet de Order
    """

    # Obtenemos los datos que queremos devolver.
    queryset = Order.objects.all()

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer']

    search_fields = ['customer']

    ordering_fields = ['id']

    def create(self, request, format=None):
        # Obtenemos todos los registros de la bd
        all_records = Order.objects.all()
        # Obtenemos la cantidad de registros de la bd
        code_db = all_records.count()
        # Sumamos 1 a la cantidad de registros de la bd
        code_db = code_db + 1
        # Añadimos ceros a la izquierda de code_db casteado a string
        code_db_str = str(code_db).zfill(5)

        # Obtenemos el año actual
        date = datetime.date.today()
        year = date.strftime("%Y")
        year_str = str(year)

        # Concatenamos el año y el numero de pedido
        order_number = year_str + code_db_str
        request.data['code'] = order_number
        serializer_class = OrderSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], name='Eliminar pedido')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False de la pedido
        """
        self.instance = self.get_object()
        if self.instance.is_active:
            super().desactivate(request)
            return Response({"message": "Entrega de pedido eliminada"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No existe ese pedido"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar pedido')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True del pedido
        """
        self.instance = self.get_object()
        if not self.instance.is_active:
            super().restore(request)
            return Response({"message": "Entrega de pedido"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ese pedido ya se encuentra activo"}, status=status.HTTP_200_OK)

class OrderDetailViewSet(BaseViewSet):
    """
    Clase ViewSet de Order
    """
    # Obtenemos los datos que queremos devolver.
    queryset = OrderDetail.objects.all()
    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = OrderDetailSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['order']

    search_fields = ['order']

    ordering_fields = ['id']

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        my_list = []
        my_dict = {}
        total = 0
        IGV = 0
        queryset = OrderDetail.objects.all()
        for i in queryset:
            IGV = 18*1/100
            total =+ i.subtotal
            my_json = {
                "ID del pedido": i.order.id,
                "Número de pedido": i.order.code,
                "Fecha de pedido": i.order.created_at,
                "Razón Social del cliente": i.order.customer.company_name,
                "Fecha de entrega": i.order.delivery.date,
                "Importe SubTotal": i.subtotal,
                "IGV": IGV,
                "Importe Total": total,
                "Importe total de descuento": 1003882
                }
            my_dict.update(my_json)
            my_list.append(my_dict)
        serializer_class = my_list
        return Response(serializer_class)

    @action(detail=True, methods=['put'], name='Eliminar detalle de pedido')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False del detalle de pedido
        """
        self.instance = self.get_object()
        if self.instance.is_active:
            super().desactivate(request)
            return Response({"message": "Entrega del detalle de pedido eliminada"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No existe ese detalle de pedido"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar detalle de pedido')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True del detalle de pedido
        """
        self.instance = self.get_object()
        if not self.instance.is_active:
            super().restore(request)
            return Response({"message": "Entrega del detalle de pedido"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ese detalle de pedido ya se encuentra activo"}, status=status.HTTP_200_OK)
