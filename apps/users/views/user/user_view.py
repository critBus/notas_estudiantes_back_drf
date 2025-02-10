from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import IsTokenValid
from apps.users.views.user.serializers.user_serializer import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsTokenValid,
    ]

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
