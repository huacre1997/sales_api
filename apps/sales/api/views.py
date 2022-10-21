from asyncio.windows_events import NULL
from venv import create
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

import datetime

class DeliveryViewSet(ModelViewSet):
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

class OrderViewSet(ModelViewSet):
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

class OrderDetailViewSet(ModelViewSet):
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

class GetDeliveryWithToken(APIView):

    def get(self, request, format=None, id = 0, *args, **kwargs):
        try:
            delivery = Delivery.objects.get(id=id)
        except Delivery.DoesNotExist:
            pass
        
        delivery_serializer = DeliverySerializer(
            delivery
        )

        payload = {
            'delivery': delivery_serializer.data
        }

        return JsonResponse(payload)

    def post(self, request, format=None):
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = DeliverySerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetOrderWithToken(APIView):

    def get(self, request, format=None, id = 0, *args, **kwargs):

        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            pass
        
        order_serializer = OrderSerializer(
            order
        )

        payload = {
            'order': order_serializer.data
        }

        return JsonResponse(payload)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = OrderSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetOrderDetailWithToken(APIView):

    def get(self, request, format=None, id = 0, *args, **kwargs):

        try:
            order_detail = OrderDetail.objects.get(id=id)
        except OrderDetail.DoesNotExist:
            pass
        
        order_detail_serializer = OrderDetailSerializer(
            order_detail
        )

        payload = {
            'order_detail': order_detail_serializer.data
        }

        return JsonResponse(payload)

    def post(self, request, format=None):
        serializer = OrderDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = OrderDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
