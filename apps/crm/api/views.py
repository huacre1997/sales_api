from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status
from rest_framework import filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from apps.crm.models import CustomerCategory, District, Customer
from apps.crm.api.serializers import CustomerCategorySerializer, DistrictSerializer, CustomerSerializer
from utils.viewsets import BaseViewSet


class CustomerCategoryViewSet(BaseViewSet):
    """
    Clase ViewSet de Customer Category
    """
    # Obtenemos los datos que queremos devolver.
    queryset = CustomerCategory.objects.all()

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = CustomerCategorySerializer

    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']

    search_fields = ['name']

    ordering_fields = ['id']

    @action(detail=True, methods=['put'], name='Eliminar categoría de cliente')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False de la categoría de cliente
        """
        self.instance = self.get_object()
        if self.instance.is_active:
            super().desactivate(request)
            return Response({"message": "Categoría de cliente eliminada"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No existe esa categoría de cliente"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar categoría')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True de la categoría de cliente
        """
        self.instance = self.get_object()
        if not self.instance.is_active:
            super().restore(request)
            return Response({"message": "Categoría de cliente restaurada"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Esa categoría de cliente ya se encuentra activa"}, status=status.HTTP_200_OK)


class DistrictViewSet(BaseViewSet):
    """
    Clase ViewSet de District
    """

    # Obtenemos los datos que queremos devolver.
    queryset = District.objects.all()

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = DistrictSerializer

    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']

    search_fields = ['name']

    ordering_fields = ['id']

    def partial_update(self, request, pk=None):
        """
        Método que actualiza parcialmente el distrito
        """
        instance = self.get_object()
        # Sobrescribimos el método y modificamos el update_by
        instance.updated_by = self.request.user
        instance.save()
        return super().partial_update(request)

    @action(detail=True, methods=['put'], name='Eliminar distritos')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False al distrito
        """
        self.instance = self.get_object()
        if self.instance.is_active:
            super().desactivate(request)
            return Response({"message": "Distrito eliminado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No existe ese distrito"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar distrito')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True del distrito
        """
        self.instance = self.get_object()
        if not self.instance.is_active:
            super().restore(self, request)
            return Response({"message": "Distrito restaurado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ese distrito ya se encuentra activo"}, status=status.HTTP_200_OK)


class CustomerViewSet(BaseViewSet):
    """
    Clase ViewSet de Customer
    """

    # Obtenemos los datos que queremos devolver.
    queryset = Customer.objects.select_related("district", "customer_category")

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = CustomerSerializer

    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company_name']

    search_fields = ['company_name']

    ordering_fields = ['id']

    @action(detail=True, methods=['put'], name='Eliminar clientes')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False al cliente
        """
        self.instance = self.get_object()
        if self.instance.is_active:
            super().desactivate(request)
            return Response({"message": "Cliente eliminado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No existe ese cliente"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar cliente')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True del cliente
        """
        self.instance = self.get_object()
        if not self.instance.is_active:
            super().restore(self, request)
            return Response({"message": "Cliente restaurado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ese cliente ya se encuentra activo"}, status=status.HTTP_200_OK)
