from django.urls import path

from apps.users.views.auth.token_authentication_view import (
    CustomTokenObtainByRSAPairView,
)
from apps.users.views.auth.token_custom_refresh_view import (
    CustomTokenRefreshView,
)
from apps.users.views.auth.token_logout_view import LogoutView

urlpatterns = [
    path("api/token/", CustomTokenObtainByRSAPairView.as_view()),
    path(
        "api/token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/token/logout/", LogoutView.as_view(), name="token_logout"),
]
