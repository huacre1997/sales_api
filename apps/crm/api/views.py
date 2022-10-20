from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from apps.crm.models import CustomerCategory,District
from apps.crm.api.serializers import CustomerCategorySerializer,DistrictSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class CustomerCategoryViewSet(ModelViewSet):
    """
    Clase ViewSet de Customer Category
    """

    # Obtenemos los datos que queremos devolver.
    queryset = CustomerCategory.objects.all()

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = CustomerCategorySerializer

    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    #permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']

    search_fields = ['name']

    ordering_fields = ['id']

class GetCustomerCategoryWithToken(APIView):

    def get(self, request, format=None, id = 0, *args, **kwargs):
        try:
            customer_category = CustomerCategory.objects.get(id=id)
        except CustomerCategory.DoesNotExist:
            pass
        
        customer_category_serializer = CustomerCategorySerializer(
            customer_category
        )

        payload = {
            'customer_category': customer_category_serializer.data
        }

        return JsonResponse(payload)

    def post(self, request, format=None):
        serializer = CustomerCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = CustomerCategorySerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DistrictViewSet(ModelViewSet):
    """
    Clase ViewSet de District
    """

    # Obtenemos los datos que queremos devolver.
    queryset = District.objects.all()

    # Le indicamos el serializer que debe utilizar para convertir los objetos a JSON.
    serializer_class = DistrictSerializer

    # Configuración para que el VIEW sea utilizado por usuarios autenticados.
    #permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']

    search_fields = ['name']

    ordering_fields = ['id']

class GetDistrictWithToken(APIView):

    def get(self, request, format=None, id = 0, *args, **kwargs):

        try:
            district = District.objects.get(id=id)
        except District.DoesNotExist:
            pass
        
        district_serializer = DistrictSerializer(
            district
        )

        payload = {
            'district': district_serializer.data
        }

        return JsonResponse(payload)

    def post(self, request, format=None):
        serializer = DistrictSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = DistrictSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)