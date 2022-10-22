from rest_framework.response import Response
from rest_framework import viewsets


class BaseViewSet(viewsets.ModelViewSet):
    """Modelo Base que heredará a todas nuestras views """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def partial_update(self, request, pk=None):
        """
        Método que actualiza parcialmente la instancia
        """
        instance = self.get_object()
        # Sobrescribimos el método y modificamos el update_by
        instance.updated_by = self.request.user
        instance.save()
        return super().partial_update(request)

    def desactivate(self, request, pk=None):
        """
        Método que cambia estado a False a la instancia
        """
        self.instance.is_active = False
        self.instance.updated_by = self.request.user
        self.instance.save()
        pass

    def restore(self, request, pk=None):
        """
        Método que cambia estado a True la instancia
        """
        self.instance.is_active = True
        self.instance.updated_by = self.request.user
        self.instance.save()
        pass
