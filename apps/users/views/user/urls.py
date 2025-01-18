from django.urls import path

from apps.users.views.user.me_view import UserMeView

urlpatterns = [
    path("user/me/", UserMeView.as_view()),
]
