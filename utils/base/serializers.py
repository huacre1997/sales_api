from rest_framework.serializers import ModelSerializer


class BaseSerializer(ModelSerializer):
    """Clase que hereradan todos nuestros Serializers"""

    def to_representation(self, obj):
        """
            Sobreescribimos el método para llamar el username y la fecha de modificación
            con un formato distinto
        """
        ret = super().to_representation(obj)
        ret["updated_by"] = obj.updated_by.username if obj.updated_by else None
        ret["updated_at"] = obj.updated_at.strftime("%d-%m-%y %H:%M:%S")
        return ret
