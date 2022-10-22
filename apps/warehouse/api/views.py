from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.warehouse.models import ProductCategory, Product
from apps.warehouse.api.serializers import ProductCategorySerializer, ProductSerializer
from utils.base.viewsets import BaseViewSet


class ProductCategoryViewSet(BaseViewSet):
    """
    Clase ViewSet de Product Category
    """
    model = ProductCategory
    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    permission_classes = (permissions.IsAuthenticated,)

    # Obtenemos los datos que queremos devolver.
    queryset = ProductCategory.objects.all()

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = ProductCategorySerializer

    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['percent_discount']

    search_fields = ['name']

    ordering_fields = ['id', 'percent_discount']

    @action(detail=True, methods=['put'], name='Eliminar categoría de producto')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False de la categoría de producto
        """
        self.instance = self.get_object()
        if self.instance.is_active:
            super().desactivate(request)
            return Response({"message": "Categoría de producto eliminada"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No existe esa categoría de producto"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar categoría de producto')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True de la categoría de producto
        """
        self.instance = self.get_object()
        if not self.instance.is_active:
            super().restore(request)
            return Response({"message": "Categoría de producto restaurada"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Esa categoría de producto ya se encuentra activa"}, status=status.HTTP_200_OK)


class ProductViewSet(BaseViewSet):
    """
    Clase ViewSet de Product
    """
    model = Product

    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    permission_classes = (permissions.IsAuthenticated,)

    # Obtenemos los datos que queremos devolver.
    queryset = Product.objects.select_related(
        "product_category", "unit_measure", "currency")

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = ProductSerializer

    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code', "name"]

    search_fields = ['name', "code"]

    ordering_fields = ['id']

    @action(detail=True, methods=['put'], name='Eliminar producto')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False del producto
        """
        self.instance = self.get_object()
        if self.instance.is_active:
            super().desactivate(request)
            return Response({"message": "Producto eliminado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No existe ese producto"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar producto')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True del producto
        """
        self.instance = self.get_object()
        if not self.instance.is_active:
            super().restore(request)
            return Response({"message": "Producto restaurado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ese producto ya se encuentra activo"}, status=status.HTTP_200_OK)
