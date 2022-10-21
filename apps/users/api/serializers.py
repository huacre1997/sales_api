from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    default_error_messages = {
        'username': 'El usuario debe contener caracteres alfanumericos'}

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        # Establece el cifrado hash en la contraseña enviada
        user.set_password(validated_data['password'])

        # Guarda el usuario
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token inválido o ha expirado')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            # Creamos un objeto Refresh Token para usar sus métodos
            token = RefreshToken(self.token)

            # Envía el refresh token a la tabla Black List donde no volverá a ser válido o utilizado
            token.blacklist()

        except TokenError:
            self.fail('bad_token')
