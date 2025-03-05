from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views.group.groups_view import GroupViewSet

router = DefaultRouter()
router.register(r"", GroupViewSet, basename="groups")

urlpatterns = [
    path("", include(router.urls)),
]
