from django.urls import include, path

urlpatterns = [
    path("token/", include("apps.users.views.auth.urls")),
    path("users/", include("apps.users.views.user.urls")),
    path("groups/", include("apps.users.views.group.urls")),
]
