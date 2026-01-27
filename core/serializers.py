from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """
    Serializer base con campos comunes del BaseModel.
    """
    
    class Meta:
        abstract = True
        fields = ['id', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BaseListSerializer(BaseSerializer):
    """
    Serializer base para operaciones de lectura (GET).
    Incluye campos detallados y relaciones.
    """
    
    class Meta(BaseSerializer.Meta):
        abstract = True


class BaseWriteSerializer(BaseSerializer):
    """
    Serializer base para operaciones de escritura (POST/PUT/PATCH).
    Solo campos necesarios para crear/actualizar.
    """
    
    class Meta(BaseSerializer.Meta):
        abstract = True
        fields = BaseSerializer.Meta.fields
        read_only_fields = BaseSerializer.Meta.read_only_fields
