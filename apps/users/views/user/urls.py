from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views.user.me_view import UserMeView
from apps.users.views.user.user_view import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
urlpatterns = [
    path("users/me/", UserMeView.as_view()),
    path("", include(router.urls)),
]
