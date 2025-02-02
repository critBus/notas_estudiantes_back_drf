from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.authentication import IsTokenValid
from apps.users.views.user.serializers.me_serializer import MeSerializer


class UserMeView(generics.GenericAPIView):
    """

    Este método requiere que el usuario esté autenticado para poder ser utilizado. La autenticación se realiza mediante el uso de una JWT (JSON Web Token) que se incluye en la cabecera de la solicitud HTTP. La JWT incluye información sobre el usuario autenticado, como su identidad y los permisos que se le han otorgado.

    Endpoint para la obtención de una entidad de User específica.
    """

    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializer_class = MeSerializer

    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
