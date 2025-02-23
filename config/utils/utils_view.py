from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, permissions, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from apps.users.authentication import IsTokenValid


class CustomPagination(PageNumberPagination):
    page_size = 10  # Define el tamaño de página predeterminado
    page_size_query_param = "page_size"  # Permite cambiar el tamaño de página con un parámetro en la URL
    max_page_size = 100  # Define el tamaño máximo de página


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="paginate",
                type=OpenApiTypes.BOOL,
                description="apply pagination to response, if not sent assume true",
                required=False,
            ),
        ],
    ),
)
class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        IsTokenValid,
    ]  # Requiere autenticación
    pagination_class = CustomPagination

    @property
    def paginator(self):
        paginate = self.request.query_params.get("paginate", None)
        if paginate is not None and paginate.lower() == "false":
            return None
        return super().paginator


class BaseGenericAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsTokenValid,
    ]  # Requiere autenticación
    pagination_class = CustomPagination

    @property
    def paginator(self):
        paginate = self.request.query_params.get("paginate", None)
        if paginate is not None and paginate.lower() == "false":
            return None
        return super().paginator


class BaseListAPIView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsTokenValid,
    ]  # Requiere autenticación
    pagination_class = CustomPagination

    @property
    def paginator(self):
        paginate = self.request.query_params.get("paginate", None)
        if paginate is not None and paginate.lower() == "false":
            return None
        return super().paginator

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="paginate",
                type=OpenApiTypes.BOOL,
                description="apply pagination to response, if not sent assume true",
                required=False,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BaseModelAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsTokenValid,
    ]
