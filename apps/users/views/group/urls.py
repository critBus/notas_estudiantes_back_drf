from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views.group.group_view import GroupViewSet

router = DefaultRouter()
router.register(r"", GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
