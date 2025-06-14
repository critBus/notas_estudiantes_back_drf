from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BlackListedTokenAccess, RefreshTokenUser

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = {
    h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES
}


def get_header(request):
    """
    Extracts the header containing the JSON web token from the given
    request.
    """
    header = request.META.get(api_settings.AUTH_HEADER_NAME)

    if isinstance(header, str):
        # Work around django test client oddness
        header = header.encode(HTTP_HEADER_ENCODING)

    return header


def get_raw_token(header):
    """
    Extracts an unvalidated JSON web token from the given "Authorization"
    header value.
    """
    parts = header.split()

    if len(parts) == 0:
        # Empty AUTHORIZATION header sent
        return None

    if parts[0] not in AUTH_HEADER_TYPE_BYTES:
        # Assume the header does not contain a JSON web token
        return None

    if len(parts) != 2:
        raise AuthenticationFailed(
            _("Authorization header must contain two space-delimited values"),
            code="bad_authorization_header",
        )

    return parts[1]


def get_acces_token(request):
    header = get_header(request)
    if header is None:
        return None
    token = get_raw_token(header)
    return token


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True

        token = get_acces_token(request)
        try:
            is_blackListed = BlackListedTokenAccess.objects.filter(
                user=user_id, token=token
            ).first()
            if is_blackListed:
                is_allowed_user = False
        except BlackListedTokenAccess.DoesNotExist:
            is_allowed_user = True
        if (
            is_allowed_user
            and RefreshTokenUser.objects.filter(
                access_token=token, vaned=True
            ).exists()
        ):
            is_allowed_user = False

        if not is_allowed_user:
            raise AuthenticationFailed("Token invalido.")
        return is_allowed_user


def logout_user(user, access_token, refresh_token=None):
    if user and access_token:
        if refresh_token is not None:
            token = RefreshToken(refresh_token)
            token.blacklist()
        RefreshToken.for_user(user)
        tokenInBD = BlackListedTokenAccess()
        tokenInBD.token = access_token
        tokenInBD.user = user
        tokenInBD.save()

        for token_bd in RefreshTokenUser.objects.filter(
            access_token=access_token
        ):
            if refresh_token is not None:
                if refresh_token != token_bd.refresh_token:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
            token_bd.vaned = True
            token_bd.save()
