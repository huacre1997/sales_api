from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer, LogoutSerializer
from rest_framework.generics import GenericAPIView


class Register(GenericAPIView):
    """Clase GenericAPIView que permite el registro de usuarios a la BD"""

    # Permite el acceso al API sin estar autenticado
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """Registro de los usuarios"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    """Clase Login que hereda de TokenObtainPairView"""
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data)
        if login_serializer.is_valid():
            # Invocamos el UserSerializer para adjuntar los datos del usuario a nuestro Response
            user = login_serializer.user

            return Response({
                "token": login_serializer.validated_data.get("access"),
                "refresh-token": login_serializer.validated_data.get("refresh"),
                "user": {
                            "username": user.username,
                            "email": user.email,
                            "name": user.first_name
                            },
                "message": "Inicio de Sesión Exitoso"
            }, status=status.HTTP_200_OK)
        # return Response({'error': 'Usuario o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):
    """Clase GenericAPIView que permite cerrar sesión y deshabilitar los refresh token """

    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Se ha cerrado la sesión'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({"message": e.args}, status=status.HTTP_400_BAD_REQUEST,)
