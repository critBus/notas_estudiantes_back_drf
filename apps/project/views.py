from rest_framework import generics, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Importa tus modelos
from .models import (
    Award,
    Career,
    Dropout,
    Graduation,
    GraduationGrade,
    Student,
    StudentCareer,
    StudentNote,
    Subject,
)

# Importa tus serializadores (debes crearlos)
from .serializers import (
    AwardSerializer,
    CareerSerializer,
    DropoutSerializer,
    GraduationGradeSerializer,
    GraduationSerializer,
    StudentCareerSerializer,
    StudentNoteSerializer,
    StudentSerializer,
    SubjectSerializer,
)


class CustomPagination(PageNumberPagination):
    page_size = 10  # Define el tamaño de página predeterminado
    page_size_query_param = "page_size"  # Permite cambiar el tamaño de página con un parámetro en la URL
    max_page_size = 100  # Define el tamaño máximo de página


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación
    pagination_class = CustomPagination  # Usa la paginación personalizada


class BaseGenericAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación
    pagination_class = CustomPagination


class StudentViewSet(BaseModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class DropoutViewSet(BaseModelViewSet):
    queryset = Dropout.objects.all()
    serializer_class = DropoutSerializer


class CareerViewSet(BaseModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer


class GraduationViewSet(BaseModelViewSet):
    queryset = Graduation.objects.all()
    serializer_class = GraduationSerializer


class GraduationGradeViewSet(BaseModelViewSet):
    queryset = GraduationGrade.objects.all()
    serializer_class = GraduationGradeSerializer


class SubjectViewSet(BaseModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class StudentNoteViewSet(BaseModelViewSet):
    queryset = StudentNote.objects.all()
    serializer_class = StudentNoteSerializer


class AwardViewSet(BaseModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer


class StudentCareerViewSet(BaseModelViewSet):
    queryset = StudentCareer.objects.all()
    serializer_class = StudentCareerSerializer


class Upgrading7and8(generics.GenericAPIView):
    queryset = Student.objects.filter(
        is_graduated=False, is_dropped_out=False, grade__in=[7, 8]
    )
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        """
        Solo para subir 7-8 (no 9)
        """
        student: Student = self.get_object()
        student.grade += 1
        student.save()
        serializer = self.get_serializer(student)
        return Response(serializer.data)
