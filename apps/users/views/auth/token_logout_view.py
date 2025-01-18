import traceback

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.authentication import IsTokenValid, get_acces_token, logout_user
from apps.users.views.auth.serializers.token_logout.token_logout_serializers import (
    TokenAccesBlacklistSerializer,
)
from config.utils.utils_exception import (
    KEY_STATUS_ERROR_CODE,
    get_first_str_exeption,
)
from config.utils.utils_logs import logger


class LogoutView(APIView):
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
                errors = get_first_str_exeption(serializer.errors)
                return Response(
                    {
                        "status": "error",
                        "message": errors,
                        KEY_STATUS_ERROR_CODE: 400,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refresh_token = serializer.validated_data["refresh"]

            user = request.user
            if user:
                logout_user(
                    user=user,
                    refresh_token=refresh_token,
                    access_token=get_acces_token(request),
                )

                # token = RefreshToken(refresh_token)
                # token.blacklist()
                # RefreshToken.for_user(user)
                # token = self.get_acces_token(request)
                # tokenInBD = BlackListedTokenAccess()
                # tokenInBD.token = token
                # tokenInBD.user = user
                # tokenInBD.save()

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
                    KEY_STATUS_ERROR_CODE: 500,
                },
                status=500,
            )
