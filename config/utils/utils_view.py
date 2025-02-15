from rest_framework import generics, permissions, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from apps.users.authentication import IsTokenValid


class CustomPagination(PageNumberPagination):
    page_size = 10  # Define el tamaño de página predeterminado
    page_size_query_param = "page_size"  # Permite cambiar el tamaño de página con un parámetro en la URL
    max_page_size = 100  # Define el tamaño máximo de página


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        IsTokenValid,
    ]  # Requiere autenticación
    pagination_class = CustomPagination


class BaseGenericAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsTokenValid,
    ]  # Requiere autenticación
    pagination_class = CustomPagination


class BaseListAPIView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsTokenValid,
    ]  # Requiere autenticación
    pagination_class = CustomPagination


class BaseModelAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsTokenValid,
    ]
