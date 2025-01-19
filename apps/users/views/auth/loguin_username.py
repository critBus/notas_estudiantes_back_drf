import traceback

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from config.utils.utils_logs import logger

from ...models import RefreshTokenUser
from ..user.serializers.user_serializer import UserSerializer
from .serializers.credentials_serializer import CredentialsSerializer
from .serializers.token_authentication_serializer import (
    AuthenticationResponseSerializer,
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        request=CredentialsSerializer,
        responses={200: AuthenticationResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        """
        Vista que obtiene un nuevo token de autenticación para un usuario en la aplicación.

        Para obtener un nuevo token de autenticación para un usuario en la aplicación, el usuario debe enviar una solicitud HTTP POST a la ruta `api/token/`. La solicitud debe incluir las credenciales del usuario (por ejemplo, su telefono y contraseña) en el cuerpo de la solicitud, y el servidor responderá con un nuevo token de autenticación válido (en el campo `access`).

        Es importante tener en cuenta que para utilizar este endpoint, el usuario debe haber proporcionado las credenciales correctas de inicio de sesión. Si las credenciales son incorrectas, entonces el servidor responderá con un error.

        """
        try:
            serializador = CredentialsSerializer(data=request.data)
            if not serializador.is_valid():
                return Response(
                    {
                        "status": "error",
                        "message": serializador.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = serializador.user
            if not user:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Credenciales incorrectas",
                    },
                    status=400,
                )

            now = timezone.now()

            user.last_login = now
            user.save()

            token = RefreshToken.for_user(user)

            access = str(token.access_token)
            refresh = str(token)

            token_bd = RefreshTokenUser()
            token_bd.refresh_token = refresh
            token_bd.access_token = access
            token_bd.user = user
            token_bd.creation_date = now
            token_bd.save()

            response = {}
            response["user"] = UserSerializer(
                user, context={"request": request}
            ).data
            response["status"] = "success"
            response["access"] = access
            response["refresh"] = refresh
            return JsonResponse(response, status=200)
        except:
            logger.error(traceback.format_exc())
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Error de en servidor",
                },
                status=500,
            )
