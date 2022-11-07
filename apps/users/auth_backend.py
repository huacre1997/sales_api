from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Clase que reemplazará a la autenticación backend por defecto    
    """
    def authenticate(self, request, **kwargs):
        user = get_user_model()
        try:
            email = kwargs.get('email', None)
            if email is None:
                email = kwargs.get('username', None)
            # Busca el email en la BD
            user = user.objects.get(email=email)
            
            # Valida el password del usuario encontrado
            if user.check_password(kwargs.get('password', None)):
                return user
        except user.DoesNotExist:
            return None
        return None
