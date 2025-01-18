from django.urls import include, path

urlpatterns = [
    path("", include("apps.users.views.user.urls")),
    path("", include("apps.users.views.auth.urls")),
]
