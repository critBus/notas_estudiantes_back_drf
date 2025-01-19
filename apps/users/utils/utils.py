import os
from uuid import uuid4

from BACKEND_NEGOCIOS.utils.utils import get_datetime_string, toBoolDefaul
from django.core.files.images import ImageFile
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User


def guardarImagenEn_Usuario(usuario: User, imagen, username):
    """
    si no hay imagen entonces elimina la que pueda existir en el DatosUsuario
    :param datosPersona:
    :param imagen:
    :param username:
    :return:
    """
    if not imagen:
        usuario.image = None
    else:
        # Obtener las extensiones de archivo originales
        _, extension1 = os.path.splitext(imagen.name)

        nuevo_nombre = (
            username
            + "_perfil_"
            + get_datetime_string()
            + "__"
            + str(uuid4())
            + str(extension1)
        )
        usuario.image = ImageFile(file=imagen, name=nuevo_nombre)
    usuario.save()


KEY_USE_APP_BUSISNESS = "useAppBusiness"


def useAppBusinessEnData(data):
    key = KEY_USE_APP_BUSISNESS  # "useAppBusiness"
    if key in data:
        return toBoolDefaul(data[key])
    # key = "esAppNegocio"
    # if key in data:
    #     return toBoolDefaul(data[key])
    return False


def comprobarYmodificarSiEsAppNegocio(response, data, usuario=None):  # =None
    if response.status_code >= 200 and response.status_code <= 299:
        if not usuario:
            username = None
            if data and "username" in data:
                username = data["username"]
                if username:
                    usuario = User.objects.filter(username=username).first()

        if usuario and useAppBusinessEnData(data):  # request,
            if not usuario.useAppBusiness:
                usuario.useAppBusiness = True
                usuario.save()
                response.data["useAppBusiness"] = True
            return True
    return False


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
