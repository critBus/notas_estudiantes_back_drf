from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import IsTokenValid
from apps.users.views.user.serializers.user_serializer import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
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
        "groups__permissions__id": ["exact"],
        "groups__permissions__name": [
            "contains",
            "exact",
            "icontains",
            "search",
        ],
        "groups__permissions__codename": [
            "contains",
            "exact",
            "icontains",
            "search",
        ],
        "user_permissions__id": ["exact"],
        "user_permissions__name": ["contains", "exact", "icontains", "search"],
        "user_permissions__codename": [
            "contains",
            "exact",
            "icontains",
            "search",
        ],
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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that
        this view requires.
        """
        permission_classes = []
        if self.action in [
            "retrieve",
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [
                IsAuthenticated,
                IsTokenValid,
            ]
        return [permission() for permission in permission_classes]
