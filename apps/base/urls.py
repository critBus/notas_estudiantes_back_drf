from django.urls import path

from .views import admin_view, logout_view

urlpatterns = [
    path("admin/logout/", logout_view),
    path("logout/", logout_view),
    path("", admin_view),
]
