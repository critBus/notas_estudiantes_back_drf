from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group  # Importa el modelo Group
from rest_framework import serializers

from apps.users.views.user.serializers.user_representantion_serializer import (
    UserRepresentationSerializer,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.ListField(
        child=serializers.CharField(), required=False
    )  # Usa ListField para listas

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "groups",
            "is_active",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_groups(self, value):
        """
        Valida que los nombres de grupos existan.
        """
        if (
            value is None
        ):  # Permite que 'groups' sea None o no esté presente en la petición
            return value

        if not isinstance(value, list):
            raise serializers.ValidationError("groups debe ser una lista.")

        group_names = set(
            value
        )  # Usar un conjunto para eficiencia en la búsqueda
        existing_groups = set(
            Group.objects.filter(name__in=value).values_list("name", flat=True)
        )

        invalid_groups = group_names - existing_groups
        if invalid_groups:
            raise serializers.ValidationError(
                f"Los siguientes grupos no existen: {', '.join(invalid_groups)}"
            )
        return value

    def create(self, validated_data):
        groups_data = validated_data.pop("groups", [])  # Extrae los grupos
        user = User.objects.create_user(
            **validated_data
        )  # Usar create_user para crear usuarios más facilmente
        # user = User(**validated_data)
        # user.set_password(validated_data["password"])
        # user.save()

        for group_name in groups_data:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop(
            "groups", None
        )  # Extrae los grupos, permite None

        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        if (
            groups_data is not None
        ):  # Solo actualiza grupos si se proporciona data
            instance.groups.clear()  # Limpia los grupos existentes si groups_data es una lista no vacía
            if groups_data:  # Añade solo si la lista no esta vacia
                for group_name in groups_data:
                    try:
                        group = Group.objects.get(name=group_name)
                        instance.groups.add(group)
                    except Group.DoesNotExist:  # Esto no deberia pasar ya que se valida antes, pero por si acaso.
                        pass
        return instance

    def to_representation(self, instance):
        return UserRepresentationSerializer(instance).data
