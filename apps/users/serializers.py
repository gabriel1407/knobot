from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.serializers import BaseListSerializer, BaseWriteSerializer
from .models import User


class UserListSerializer(BaseListSerializer):
    """
    Serializer para listar usuarios (GET).
    Incluye información detallada.
    """
    
    class Meta(BaseListSerializer.Meta):
        model = User
        fields = BaseListSerializer.Meta.fields + [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
            'company',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
        ]
        read_only_fields = BaseListSerializer.Meta.read_only_fields + [
            'username',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
        ]


class UserWriteSerializer(BaseWriteSerializer):
    """
    Serializer para crear/actualizar usuarios (POST/PUT/PATCH).
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta(BaseWriteSerializer.Meta):
        model = User
        fields = BaseWriteSerializer.Meta.fields + [
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'phone',
            'role',
            'company',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }
    
    def validate(self, attrs):
        """
        Validar que las contraseñas coincidan.
        """
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden'
            })
        return attrs
    
    def create(self, validated_data):
        """
        Crear usuario con contraseña encriptada.
        """
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user
    
    def update(self, instance, validated_data):
        """
        Actualizar usuario, manejando contraseña si se proporciona.
        """
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        # Actualizar campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Actualizar contraseña si se proporcionó
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para el perfil del usuario autenticado.
    """
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
            'company',
            'created_at',
            'last_login',
        ]
        read_only_fields = ['id', 'username', 'role', 'created_at', 'last_login']
