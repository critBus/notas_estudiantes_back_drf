import traceback

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from apps.users.authentication import IsTokenValid, get_acces_token
from apps.users.models import BlackListedTokenAccess
from apps.users.views.auth.serializers.logout.token_acces_blacklist_serializer import (
    TokenAccesBlacklistSerializer,
)
from config.utils.utils_logs import logger


class Logout(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )

    @extend_schema(
        request=TokenAccesBlacklistSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Vista que invalida un token de autenticación de un usuario en la aplicación.
        """
        try:
            serializer = TokenAccesBlacklistSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "status": "error",
                        "message": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refresh_token = serializer.validated_data["refresh"]

            user = request.user
            if user:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except TokenError:
                    pass
                RefreshToken.for_user(user)
                token = get_acces_token(request)
                tokenInBD = BlackListedTokenAccess()
                tokenInBD.token = token
                tokenInBD.user = user
                tokenInBD.save()

                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Sesión cerrada correctamente.",
                    },
                    status=status.HTTP_200_OK,
                )
            return JsonResponse(
                {"status": "error", "message": "No existe este usuario."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Error en servidor",
                },
                status=500,
            )
