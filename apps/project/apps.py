from django.apps import AppConfig
from django.db.models.signals import post_migrate


def config_app(sender, **kwargs):
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    from apps.project.models import ROL_NAME_ADMIN
    from apps.project.utils.util_reporte_d import load_automatic_reports

    from .utils.nomencladores import crear_roles_django_default

    User = get_user_model()
    crear_roles_django_default()
    if User.objects.all().count() == 0:
        user = User.objects.create_superuser(
            username=settings.DJANGO_SUPERUSER_USERNAME,
            email=settings.DJANGO_SUPERUSER_EMAIL,
            first_name=settings.DJANGO_SUPERUSER_FIRST_NAME,
            last_name=settings.DJANGO_SUPERUSER_LAST_NAME,
            password=settings.DJANGO_SUPERUSER_PASSWORD,
        )
        user.groups.add(Group.objects.get(name=ROL_NAME_ADMIN))

    load_automatic_reports()

    if settings.LOAD_EXAMPLE_DATA:
        from apps.project.utils.utils_ejemplos import crear_datos_random

        crear_datos_random()


class ProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.project"

    def ready(self):
        post_migrate.connect(config_app, sender=self)
