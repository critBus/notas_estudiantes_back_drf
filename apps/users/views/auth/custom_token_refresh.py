from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """
        Vista que renueva el token de autenticación de un usuario que ya ha iniciado sesión en la aplicación.

        Para renovar el token, el usuario debe enviar una solicitud HTTP POST a la ruta `api/token/refresh/`. La solicitud debe incluir el token de autenticación expirado en el cuerpo de la solicitud (en el campo `refresh`), y el servidor responderá con un nuevo token de autenticación válido (en el campo `access`).

        Es importante tener en cuenta que para utilizar este endpoint, el usuario debe haber iniciado sesión previamente en la aplicación y haber recibido un token de autenticación válido. Si el usuario no tiene un token de autenticación válido, entonces no podrá renovarlo y deberá iniciar sesión de nuevo.

        Esta vista es proporcionada por la librería `django-rest-framework-simplejwt`, la cual implementa el estándar JSON Web Tokens (JWT) para la autenticación de usuarios en API RESTful.

        """
        return super().post(request, *args, **kwargs)
