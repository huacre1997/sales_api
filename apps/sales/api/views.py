from django.db.models.functions import Round
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from apps.sales.models import Delivery, Order, OrderDetail
from apps.sales.api.serializers import DeliverySerializer, OrderSerializer, OrderDetailSerializer, OrderSearchSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Subquery, OuterRef, Sum, F
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

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['address']

    search_fields = ['address']

    ordering_fields = ['-id']

    permission_classes = (IsAuthenticated,)

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


class OrderViewSet(ModelViewSet):
    """
    Clase ViewSet de Order
    """

    # Obtenemos los datos que queremos devolver.
    queryset = Order.objects.all()

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = OrderSerializer

    filter_backends = [filters.OrderingFilter]

    ordering_fields = ['id']

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Sobreescribimos el método con nuestro queryset personalizado"""

        # Será utilizado para filtrar nuestra qs según lo params enviados
        filtros = {}

        # Capturamos los query params dela url
        code = self.request.query_params.get('code')
        date = self.request.query_params.get('date')
        totalAmountHigherThan = self.request.query_params.get(
            "totalAmountHigherThan")

        # Generamos un dict con los query params
        if code:
            filtros["code"] = code
        if date:
            filtros["date"] = date
        if totalAmountHigherThan:
            filtros["total__gte"] = totalAmountHigherThan

        """{"code":1213123,"date":"21-22-22"}"""
        # annotate -> Agrega una columna extra al queryset
        # select_related -> Permite realizar una sola vez la consulta de algún FK
        # Subquery -> Permite agregar una subquery a nuestra queryset
        # F -> Permite seleccionar los valores de la misma qs en otro cálculos que se necesiten
        # Sum -> Permite realizar sumas de un conjunto de valores
        # Round -> Permite rendondear valores de la qs
        s_qs = OrderDetail.objects.select_related("order").filter(
            order_id=OuterRef('pk')).values("order_id").annotate(total_discount=Sum("discount_amount")).annotate(total_subtotal=Sum("subtotal"))
        qs = (super().get_queryset().select_related("delivery", "customer")
              .annotate(total_discount=Subquery(s_qs.values('total_discount')[:1]))
              .annotate(total_subtotal=Subquery(s_qs.values('total_subtotal')[:1]))
              .annotate(total_igv=Round(F("total_subtotal") * 18 / 100))
              .annotate(total=Round(F("total_subtotal") + F("total_igv"), precision=2))
              ).filter(**filtros)
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrderSearchSerializer(instance)
        return Response(serializer.data)

    def paginate(self, queryset):
        """
            Genera el queryset paginado y lo envolvemos en una Respuesta.
        """
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request):
        "Método que lista el queryset paginado"
        queryset = self.get_queryset()
        return self.paginate(queryset)

    def create(self, request, format=None):
        try:
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
            # Concatenamos el año actual y el codigo
            order_number = year_str + code_db_str
            # Validamos los delivery
            serializer_delivery = DeliverySerializer(
                data=request.data["delivery"])
            if serializer_delivery.is_valid():
                delivery = serializer_delivery.save()
            else:
                return Response(serializer_delivery.errors, status=status.HTTP_400_BAD_REQUEST)
            order = Order()
            order.code = order_number
            order.customer_id = request.data["cliente"]
            order.date = request.data["date"]
            order.delivery = delivery
            order.save()
            for i in (request.data["details"]):
                obj = {
                    "product": i["product"],
                    "quantity": i["quantity"],
                    "order": order.id
                }
                # Validamos el detalle de orden
                serializer_detail = OrderDetailSerializer(data=obj)
                if serializer_detail.is_valid():
                    serializer_detail.save()
                else:
                    return Response(serializer_detail.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"mensaje": "Orden creada exitosamente"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({"mensaje": "Ha ocurrido un error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
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
            IGV = 18 * 1 / 100
            total = + i.subtotal
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
