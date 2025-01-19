from django.urls import path

from .custom_token_refresh import CustomTokenRefreshView
from .custom_token_verify import CustomTokenVerifyView
from .logout import Logout
from .loguin_username import CustomTokenObtainPairView

urlpatterns = [
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/token/verify/",
        CustomTokenVerifyView.as_view(),
        name="token_verify",
    ),
    path("api/token/logout/", Logout.as_view(), name="token_logout"),
]
