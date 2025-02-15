from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import generics, serializers
from rest_framework.response import Response

from config.utils.utils_view import (
    BaseGenericAPIView,
    BaseListAPIView,
    BaseModelAPIView,
    BaseModelViewSet,
)

# Importa tus modelos
from .models import (
    Award,
    Career,
    DegreeScale,
    Dropout,
    Graduation,
    GraduationGrade,
    SchoolYear,
    Student,
    StudentCareer,
    StudentNote,
    Subject,
)

# Importa tus serializadores (debes crearlos)
from .serializers import (
    AwardSerializer,
    BallotCreateSerializer,
    CareerSerializer,
    DegreeScaleSerializer,
    DropoutSerializer,
    ErrorSerializer,
    GraduationGradeSerializer,
    GraduationSerializer,
    SchoolYearSerializer,
    StudentBallotSerializer,
    StudentCareerSerializer,
    StudentNoteSerializer,
    StudentSerializer,
    SubjectSerializer,
)


class SchoolYearViewSet(BaseModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer


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


class DegreeScaleViewSet(BaseModelViewSet):
    queryset = DegreeScale.objects.all()
    serializer_class = DegreeScaleSerializer


class Upgrading7and8(generics.GenericAPIView):
    queryset = Student.objects.filter(
        is_graduated=False, is_dropped_out=False, grade__in=[7, 8]
    )
    serializer_class = StudentSerializer

    @extend_schema(
        responses={
            200: StudentSerializer,
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Solo para subir 7-8 (no 9)
        """
        student: Student = self.get_object()
        if student.their_notes_are_valid():
            student.grade += 1
            student.save()
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        return JsonResponse(
            {"error": "Tiene notas que no son validas"}, status=400
        )


class CurrentCurseView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: SchoolYearSerializer,
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        course = SchoolYear.get_current_course()
        if not course:
            return JsonResponse(
                {"error": "No hay cursos agregados"}, status=400
            )
        return SchoolYearSerializer(course).data


class BallotCreateView(BaseGenericAPIView):
    queryset = Student.objects.filter(
        is_graduated=False, is_dropped_out=False, grade__in=[7, 8]
    )
    serializer_class = BallotCreateSerializer

    @extend_schema(
        responses={
            200: StudentBallotSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        student: Student = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        list_career = serializer.validated_data["list_career_name"]
        student.create_ballot(list_career)
        return JsonResponse(StudentBallotSerializer(student).data)

    @extend_schema(
        responses={
            200: serializers.ListSerializer(child=serializers.CharField())
        },
    )
    def get(self, request, *args, **kwargs):
        student: Student = self.get_object()
        return JsonResponse(student.get_ballot(), safe=False)


class BallotListView(BaseListAPIView):
    queryset = Student.objects.filter(
        is_graduated=False, is_dropped_out=False, grade__in=[7, 8]
    )
    serializer_class = StudentBallotSerializer


class DegreeScaleCalculateView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: DegreeScaleSerializer(many=True),
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            score = DegreeScale.calculate_all_ranking_number()
            return JsonResponse(
                DegreeScaleSerializer(score, many=True).data, safe=False
            )
        except serializers.ValidationError as e:
            return JsonResponse({"error": e.detail}, status=400)


class DegreeScaleCurrentView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: DegreeScaleSerializer(many=True),
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        score = DegreeScale.current()
        return JsonResponse(
            DegreeScaleSerializer(score, many=True).data, safe=False
        )
