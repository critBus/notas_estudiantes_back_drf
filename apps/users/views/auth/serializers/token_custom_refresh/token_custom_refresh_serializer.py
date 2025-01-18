from crum import get_current_request
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from apps.users.authentication import get_acces_token
from apps.users.models import RefreshTokenUser


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        old_refresh_token = attrs["refresh"]
        data = super().validate(attrs)
        request = get_current_request()
        old_access_token = get_acces_token(request)
        user = None
        if old_access_token:
            q = RefreshTokenUser.objects.filter(refresh_token=old_refresh_token)
            q.update(vaned=True)
            old_token_bd: RefreshTokenUser = q.filter(
                user__isnull=False
            ).first()
            if old_token_bd:
                user = old_token_bd.user

        token_bd = RefreshTokenUser()
        token_bd.refresh_token = data["refresh"]
        token_bd.access_token = data["access"]
        token_bd.user = user
        token_bd.creation_date = timezone.now()
        token_bd.save()
        return data
