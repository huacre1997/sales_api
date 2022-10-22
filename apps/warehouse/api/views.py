from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status
from rest_framework import filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from apps.warehouse.models import ProductCategory
from apps.warehouse.api.serializers import ProductCategorySerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    Clase ViewSet de Product Category
    """
    model = ProductCategory
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

    def list(self, request):
        """
        Método que lista las categrorías de productos con estado True
        """
        data = self.get_queryset().filter(is_active=True)
        data = self.get_serializer(data, many=True)
        return Response(data.data)

    @action(detail=True, methods=['put'], name='Eliminar categoría de producto')
    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False de la categoría de producto
        """
        instance = self.get_object()
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save()
        return Response({"message": "Categoría eliminada"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], name='Restaurar categoría')
    def restore(self, request, pk=None):
        """
        Método que cambia estado a True de la categoría de producto
        """
        instance = self.get_object()
        instance.is_active = True
        instance.updated_by = self.request.user
        instance.save()
        return Response({"message": "Categoría restaurada"}, status=status.HTTP_200_OK)
