from rest_framework_simplejwt.views import TokenBlacklistView


class CustomTokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        """
        Vista que invalida un token de autenticación de un usuario en la aplicación.

        Para invalidar un token de autenticación de un usuario en la aplicación, el usuario debe enviar una solicitud HTTP POST a la ruta `api/token/blacklist/`. La solicitud debe incluir el token de autenticación en el cuerpo de la solicitud (en el campo `token`), y el servidor responderá con una respuesta HTTP que indica si el token ha sido invalidado correctamente.

        Es importante tener en cuenta que al invalidar un token de autenticación, el usuario ya no podrá utilizarlo para acceder a la aplicación. Por lo tanto, es necesario tener cuidado al utilizar este endpoint para no invalidar accidentalmente tokens que todavía son válidos.

        Esta vista es proporcionada por la librería `django-rest-framework-simplejwt`, la cual implementa el estándar JSON Web Tokens (JWT) para la autenticación de usuarios en API RESTful.

        """
        return super().post(request, *args, **kwargs)
