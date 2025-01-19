from rest_framework_simplejwt.views import TokenVerifyView


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        """
        Vista que verifica la validez de un token de autenticación de un usuario en la aplicación.

        Para verificar la validez de un token de autenticación de un usuario en la aplicación, el usuario debe enviar una solicitud HTTP POST a la ruta `api/token/verify/`. La solicitud debe incluir el token de autenticación en el cuerpo de la solicitud (en el campo `token`), y el servidor responderá con una respuesta HTTP que indica si el token es válido o no.

        Es importante tener en cuenta que para utilizar este endpoint, el usuario debe haber iniciado sesión previamente en la aplicación y haber recibido un token de autenticación válido. Si el usuario no tiene un token de autenticación válido, entonces no podrá verificar su validez.

        Esta vista es proporcionada por la librería `django-rest-framework-simplejwt`, la cual implementa el estándar JSON Web Tokens (JWT) para la autenticación de usuarios en API RESTful.

        """
        return super().post(request, *args, **kwargs)
