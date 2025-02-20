from django.http import JsonResponse
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, serializers
from rest_framework.response import Response

from config.utils.utils_view import (
    BaseGenericAPIView,
    BaseListAPIView,
    BaseModelAPIView,
    BaseModelViewSet,
)

from .models import (
    Career,
    DegreeScale,
    Dropout,
    GrantCareer,
    SchoolYear,
    Student,
    StudentCareer,
    StudentNote,
    Subject,
)
from .serializers import (
    BallotCreateSerializer,
    CareerSerializer,
    DegreeScaleSerializer,
    DropoutRepresentationSerializer,
    DropoutSerializer,
    ErrorSerializer,
    GrantCareerSerializer,
    SchoolYearSerializer,
    StudentBallotSerializer,
    StudentCareerSerializer,
    StudentNoteRepresentationSerializer,
    StudentNoteSerializer,
    StudentSerializer,
    SubjectSerializer,
)


class GrantCareerViewSet(BaseModelViewSet):
    queryset = GrantCareer.objects.all()
    serializer_class = GrantCareerSerializer


class SchoolYearViewSet(BaseModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer

    filterset_fields = {
        "id": ["exact"],
        "name": ["contains", "exact", "icontains", "search"],
        "start_date": ["gte", "lte", "gt", "lt", "exact"],
        "end_date": ["gte", "lte", "gt", "lt", "exact"],
    }
    search_fields = [
        "name",
    ]
    ordering_fields = [
        "pk",
        "name",
        "start_date",
        "end_date",
    ]
    ordering = ["start_date"]


class StudentViewSet(BaseModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    filterset_fields = {
        "id": ["exact"],
        "ci": ["contains", "exact", "icontains", "search"],
        "address": ["contains", "exact", "icontains", "search"],
        "grade": ["exact"],
        "first_name": ["contains", "exact", "icontains", "search"],
        "last_name": ["contains", "exact", "icontains", "search"],
        "registration_number": ["contains", "exact", "icontains", "search"],
        "sex": ["exact"],
        "is_graduated": ["exact"],
        "is_dropped_out": ["exact"],
    }
    search_fields = [
        "address",
        "registration_number",
        "first_name",
        "last_name",
    ]
    ordering_fields = [
        "pk",
        "ci",
        "address",
        "grade",
        "first_name",
        "last_name",
        "registration_number",
        "sex",
        "is_graduated",
        "is_dropped_out",
    ]
    ordering = ["ci"]


@extend_schema_view(
    list=extend_schema(responses=DropoutRepresentationSerializer(many=True)),
    create=extend_schema(responses=DropoutRepresentationSerializer),
    retrieve=extend_schema(responses=DropoutRepresentationSerializer),
    update=extend_schema(responses=DropoutRepresentationSerializer),
    partial_update=extend_schema(responses=DropoutRepresentationSerializer),
)
class DropoutViewSet(BaseModelViewSet):
    queryset = Dropout.objects.all()
    serializer_class = DropoutSerializer

    filterset_fields = {
        "id": ["exact"],
        "municipality": ["contains", "exact", "icontains", "search"],
        "date": ["gte", "lte", "gt", "lt", "exact"],
        "province": ["contains", "exact", "icontains", "search"],
        "school": ["contains", "exact", "icontains", "search"],
        "student": ["exact"],
        "student__ci": ["contains", "exact", "icontains", "search"],
        "student__address": ["contains", "exact", "icontains", "search"],
        "student__grade": ["exact"],
        "student__first_name": ["contains", "exact", "icontains", "search"],
        "student__last_name": ["contains", "exact", "icontains", "search"],
        "student__registration_number": [
            "contains",
            "exact",
            "icontains",
            "search",
        ],
        "student__sex": ["exact"],
        "student__is_graduated": ["exact"],
        "student__is_dropped_out": ["exact"],
    }
    search_fields = [
        "student__ci",
    ]
    ordering_fields = [
        "pk",
        "municipality",
        "province",
        "school",
        "student__ci",
        "student__first_name",
        "student__last_name",
    ]
    ordering = ["student__ci"]


class CareerViewSet(BaseModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

    filterset_fields = {
        "id": ["exact"],
        "name": ["contains", "exact", "icontains", "search"],
        "amount": ["gte", "lte", "gt", "lt", "exact"],
    }
    search_fields = [
        "name",
    ]
    ordering_fields = [
        "pk",
        "name",
        "amount",
    ]
    ordering = ["name"]


class SubjectViewSet(BaseModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    filterset_fields = {
        "id": ["exact"],
        "name": ["contains", "exact", "icontains", "search"],
        "grade": ["exact"],
        "tcp2_required": ["exact"],
    }
    search_fields = [
        "name",
    ]
    ordering_fields = [
        "pk",
        "name",
        "grade",
        "tcp2_required",
    ]
    ordering = ["name"]


@extend_schema_view(
    list=extend_schema(
        responses=StudentNoteRepresentationSerializer(many=True)
    ),
    create=extend_schema(responses=StudentNoteRepresentationSerializer),
    retrieve=extend_schema(responses=StudentNoteRepresentationSerializer),
    update=extend_schema(responses=StudentNoteRepresentationSerializer),
    partial_update=extend_schema(responses=StudentNoteRepresentationSerializer),
)
class StudentNoteViewSet(BaseModelViewSet):
    queryset = StudentNote.objects.all()
    serializer_class = StudentNoteSerializer

    filterset_fields = {
        "id": ["exact"],
        "student": ["exact"],
        "student__ci": ["contains", "exact", "icontains", "search"],
        "student__address": ["contains", "exact", "icontains", "search"],
        "student__grade": ["exact"],
        "student__first_name": ["contains", "exact", "icontains", "search"],
        "student__last_name": ["contains", "exact", "icontains", "search"],
        "student__registration_number": [
            "contains",
            "exact",
            "icontains",
            "search",
        ],
        "student__sex": ["exact"],
        "student__is_graduated": ["exact"],
        "student__is_dropped_out": ["exact"],
        "subject": ["exact"],
        "subject__name": ["contains", "exact", "icontains", "search"],
        "subject__grade": ["exact"],
        "subject__tcp2_required": ["exact"],
        "school_year": ["exact"],
        "school_year__name": ["contains", "exact", "icontains", "search"],
        "school_year__start_date": ["gte", "lte", "gt", "lt", "exact"],
        "school_year__end_date": ["gte", "lte", "gt", "lt", "exact"],
        "asc": ["gte", "lte", "gt", "lt", "exact"],
        "final_grade": ["gte", "lte", "gt", "lt", "exact"],
        "final_exam": ["gte", "lte", "gt", "lt", "exact"],
        "tcp1": ["gte", "lte", "gt", "lt", "exact"],
        "tcp2": ["gte", "lte", "gt", "lt", "exact"],
    }

    ordering_fields = [
        "pk",
        "school_year__start_date",
        "school_year__end_date",
        "asc",
        "final_grade",
        "final_exam",
        "tcp1",
        "tcp2",
    ]
    ordering = ["pk"]


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
        is_graduated=False, is_dropped_out=False, grade=9
    )
    serializer_class = BallotCreateSerializer

    @extend_schema(
        responses={
            201: StudentBallotSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        student: Student = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        list_career = serializer.validated_data["list_career_name"]
        student.create_ballot(list_career)
        return JsonResponse(StudentBallotSerializer(student).data, status=201)

    @extend_schema(
        examples=[
            OpenApiExample(
                "Carreras seleccionadas",
                value=[
                    "career19",
                    "career0",
                    "career1",
                    "career2",
                    "career3",
                    "career4",
                    "career5",
                    "career6",
                    "career7",
                    "career8",
                ],
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        student: Student = self.get_object()
        return JsonResponse(student.get_ballot(), safe=False)


class BallotListView(BaseListAPIView):
    queryset = Student.objects.filter(
        is_graduated=False, is_dropped_out=False, grade=9
    )
    serializer_class = StudentBallotSerializer

    filterset_fields = {
        "id": ["exact"],
        "ci": ["contains", "exact", "icontains", "search"],
        "address": ["contains", "exact", "icontains", "search"],
        "grade": ["exact"],
        "first_name": ["contains", "exact", "icontains", "search"],
        "last_name": ["contains", "exact", "icontains", "search"],
        "registration_number": ["contains", "exact", "icontains", "search"],
        "sex": ["exact"],
        "is_graduated": ["exact"],
        "is_dropped_out": ["exact"],
    }
    search_fields = [
        "address",
        "registration_number",
        "first_name",
        "last_name",
    ]
    ordering_fields = [
        "pk",
        "ci",
        "address",
        "grade",
        "first_name",
        "last_name",
        "registration_number",
        "sex",
        "is_graduated",
        "is_dropped_out",
    ]
    ordering = ["ci"]


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


class CarryOutGrantingOfCoursesView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: GrantCareerSerializer(many=True),
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        grants = GrantCareer.grant()
        return JsonResponse(
            GrantCareerSerializer(grants, many=True).data, safe=False
        )


class GrantCareerCurrentView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: GrantCareerSerializer(many=True),
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        grants = GrantCareer.current()
        return JsonResponse(
            GrantCareerSerializer(grants, many=True).data, safe=False
        )
