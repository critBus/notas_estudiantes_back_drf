from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.users.views.user.serializers.user_representantion_serializer import (
    UserRepresentationSerializer,
)
from apps.users.views.user.serializers.user_serializer import UserSerializer
from config.utils.utils_view import BaseModelViewSet

User = get_user_model()


@extend_schema_view(
    list=extend_schema(responses=UserRepresentationSerializer(many=True)),
    create=extend_schema(responses=UserRepresentationSerializer),
    retrieve=extend_schema(responses=UserRepresentationSerializer),
    update=extend_schema(responses=UserRepresentationSerializer),
    partial_update=extend_schema(responses=UserRepresentationSerializer),
)
class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filterset_fields = {
        "id": ["exact"],
        "last_login": ["gte", "lte", "gt", "lt", "exact"],
        "is_superuser": ["exact"],
        "username": ["contains", "exact", "icontains", "search"],
        "email": ["contains", "exact", "icontains", "search"],
        "first_name": ["contains", "exact", "icontains", "search"],
        "last_name": ["contains", "exact", "icontains", "search"],
        "is_active": ["exact"],
        "is_staff": ["exact"],
        "groups__id": ["exact"],
        "groups__name": ["contains", "exact", "icontains", "search"],
    }
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
    ]
    ordering_fields = [
        "pk",
        "last_login",
        "username",
        "email",
        "first_name",
        "last_name",
    ]
    ordering = ["username"]
