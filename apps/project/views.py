from django.http import JsonResponse
from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from config.utils.utils_view import (
    BaseGenericAPIView,
    BaseListAPIView,
    BaseModelAPIView,
    BaseModelViewSet,
)

from .models import (
    ROL_NAME_ADMIN,
    ROL_NAME_PROFESSOR,
    ROL_NAME_STUDENT,
    ApprovedSchoolCourse,
    Career,
    DegreeScale,
    Dropout,
    FileFolder,
    FileSchoolTask,
    FileStudentResponse,
    Folder,
    GrantCareer,
    Professor,
    SchoolEvent,
    SchoolTask,
    SchoolYear,
    Student,
    StudentCareer,
    StudentNote,
    StudentResponse,
    Subject,
    SubjectSection,
)
from .serializers.general import (
    ApprovedSchoolCourseRepresentationSerializer,
    ApprovedSchoolCourseSerializer,
    BallotCreateSerializer,
    CareerSerializer,
    DegreeScaleSerializer,
    DropoutRepresentationSerializer,
    DropoutSerializer,
    ErrorSerializer,
    FileFolderRepresentationSerializer,
    FileFolderSerializer,
    FileSchoolTaskRepresentationSerializer,
    FileSchoolTaskSerializer,
    FileStudentResponseRepresentationSerializer,
    FileStudentResponseSerializer,
    FolderRepresentationSerializer,
    FolderSerializer,
    GrantCareerRepresentationSerializer,
    GrantCareerSerializer,
    ProfessorCreateSerializer,
    ProfessorSerializer,
    ProfessorUpdateSerializer,
    SchoolEventSerializer,
    SchoolTaskRepresentationSerializer,
    SchoolTaskSerializer,
    SchoolYearSerializer,
    StudentBallotSerializer,
    StudentCareerSerializer,
    StudentCreateSerializer,
    StudentNoteRepresentationSerializer,
    StudentNoteSerializer,
    StudentResponseRepresentationSerializer,
    StudentResponseSerializer,
    StudentSerializer,
    StudentUpdateSerializer,
    SubjectRepresentationSerializer,
    SubjectSectionRepresentationSerializer,
    SubjectSectionSerializer,
    SubjectSerializer,
)
from .serializers.student_response.create import StudentResponseCreateSerializer
from .serializers.subject_section.create import SubjectSectionCreateSerializer
from .serializers.subject_section.representation import (
    SubjectSectionCreateRepresentationSerializer,
)
from .utils.extenciones import get_extension


class SchoolEventViewSet(BaseModelViewSet):
    queryset = SchoolEvent.objects.all()
    serializer_class = SchoolEventSerializer

    filterset_fields = {
        "id": ["exact"],
        "title": ["contains", "exact", "icontains", "search"],
        "date": ["gte", "lte", "gt", "lt", "exact"],
        "description": ["contains", "exact", "icontains", "search"],
    }
    search_fields = ["title", "description"]
    ordering_fields = [
        "pk",
        "title",
        "date",
    ]
    ordering = ["date"]


# @extend_schema_view(
#     list=extend_schema(
#         responses=ProfessorEvaluationRepresentationSerializer(many=True)
#     ),
#     create=extend_schema(responses=ProfessorEvaluationRepresentationSerializer),
#     retrieve=extend_schema(
#         responses=ProfessorEvaluationRepresentationSerializer
#     ),
#     update=extend_schema(responses=ProfessorEvaluationRepresentationSerializer),
#     partial_update=extend_schema(
#         responses=ProfessorEvaluationRepresentationSerializer
#     ),
# )
# class ProfessorEvaluationViewSet(BaseModelViewSet):
#     queryset = ProfessorEvaluation.objects.all()
#     serializer_class = ProfessorEvaluationSerializer


@extend_schema_view(
    list=extend_schema(
        responses=FileStudentResponseRepresentationSerializer(many=True)
    ),
    create=extend_schema(responses=FileStudentResponseRepresentationSerializer),
    retrieve=extend_schema(
        responses=FileStudentResponseRepresentationSerializer
    ),
    update=extend_schema(responses=FileStudentResponseRepresentationSerializer),
    partial_update=extend_schema(
        responses=FileStudentResponseRepresentationSerializer
    ),
)
class StudentResponseViewSet(BaseModelViewSet):
    queryset = FileStudentResponse.objects.all()
    serializer_class = FileStudentResponseSerializer


@extend_schema_view(
    list=extend_schema(
        responses=StudentResponseRepresentationSerializer(many=True)
    ),
    create=extend_schema(
        request=StudentResponseCreateSerializer,
        responses=StudentResponseRepresentationSerializer,
    ),
    retrieve=extend_schema(responses=StudentResponseRepresentationSerializer),
    update=extend_schema(responses=StudentResponseRepresentationSerializer),
    partial_update=extend_schema(
        responses=StudentResponseRepresentationSerializer
    ),
)
class StudentResponseViewSet(BaseModelViewSet):
    queryset = StudentResponse.objects.all()
    serializer_class = StudentResponseSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return StudentResponseCreateSerializer
        return self.serializer_class


@extend_schema_view(
    list=extend_schema(
        responses=FileSchoolTaskRepresentationSerializer(many=True)
    ),
    create=extend_schema(responses=FileSchoolTaskRepresentationSerializer),
    retrieve=extend_schema(responses=FileSchoolTaskRepresentationSerializer),
    update=extend_schema(responses=FileSchoolTaskRepresentationSerializer),
    partial_update=extend_schema(
        responses=FileSchoolTaskRepresentationSerializer
    ),
)
class FileSchoolTaskViewSet(BaseModelViewSet):
    queryset = FileSchoolTask.objects.all()
    serializer_class = FileSchoolTaskSerializer


@extend_schema_view(
    list=extend_schema(responses=SchoolTaskRepresentationSerializer(many=True)),
    create=extend_schema(responses=SchoolTaskRepresentationSerializer),
    retrieve=extend_schema(responses=SchoolTaskRepresentationSerializer),
    update=extend_schema(responses=SchoolTaskRepresentationSerializer),
    partial_update=extend_schema(responses=SchoolTaskRepresentationSerializer),
)
class SchoolTaskViewSet(BaseModelViewSet):
    queryset = SchoolTask.objects.all()
    serializer_class = SchoolTaskSerializer


@extend_schema_view(
    list=extend_schema(responses=FileFolderRepresentationSerializer(many=True)),
    create=extend_schema(responses=FileFolderRepresentationSerializer),
    retrieve=extend_schema(responses=FileFolderRepresentationSerializer),
    update=extend_schema(responses=FileFolderRepresentationSerializer),
    partial_update=extend_schema(responses=FileFolderRepresentationSerializer),
)
class FileFolderViewSet(BaseModelViewSet):
    queryset = FileFolder.objects.all()
    serializer_class = FileFolderSerializer


@extend_schema_view(
    list=extend_schema(responses=FolderRepresentationSerializer(many=True)),
    create=extend_schema(responses=FolderRepresentationSerializer),
    retrieve=extend_schema(responses=FolderRepresentationSerializer),
    update=extend_schema(responses=FolderRepresentationSerializer),
    partial_update=extend_schema(responses=FolderRepresentationSerializer),
)
class FolderViewSet(BaseModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


@extend_schema_view(
    list=extend_schema(
        responses=SubjectSectionRepresentationSerializer(many=True)
    ),
    create=extend_schema(responses=SubjectSectionRepresentationSerializer),
    retrieve=extend_schema(responses=SubjectSectionRepresentationSerializer),
    update=extend_schema(responses=SubjectSectionRepresentationSerializer),
    partial_update=extend_schema(
        responses=SubjectSectionRepresentationSerializer
    ),
)
class SubjectSectionViewSet(BaseModelViewSet):
    queryset = SubjectSection.objects.all()
    serializer_class = SubjectSectionSerializer


@extend_schema_view(
    create=extend_schema(request=ProfessorCreateSerializer),
    update=extend_schema(request=ProfessorUpdateSerializer),
    partial_update=extend_schema(request=ProfessorUpdateSerializer),
)
class ProfessorViewSet(BaseModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    filterset_fields = {
        "id": ["exact"],
        "ci": ["contains", "exact", "icontains", "search"],
        "address": ["contains", "exact", "icontains", "search"],
        "first_name": ["contains", "exact", "icontains", "search"],
        "last_name": ["contains", "exact", "icontains", "search"],
        "sex": ["exact"],
        "user": ["isnull"],
        "user__id": ["exact"],
        "user__last_login": ["gte", "lte", "gt", "lt", "exact"],
        "user__is_superuser": ["exact"],
        "user__username": ["contains", "exact", "icontains", "search"],
        "user__email": ["contains", "exact", "icontains", "search"],
        "user__first_name": ["contains", "exact", "icontains", "search"],
        "user__last_name": ["contains", "exact", "icontains", "search"],
        "user__is_active": ["exact"],
        "user__is_staff": ["exact"],
        "user__groups__id": ["exact"],
        "user__groups__name": ["contains", "exact", "icontains", "search"],
    }
    search_fields = [
        "address",
        "first_name",
        "last_name",
        "user__username",
        "user__email",
    ]
    ordering_fields = [
        "pk",
        "ci",
        "address",
        "first_name",
        "last_name",
        "sex",
        "user__username",
        "user__email",
    ]
    ordering = ["ci"]

    def get_serializer_class(self):
        if self.action == "create":
            return ProfessorCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return ProfessorUpdateSerializer
        return self.serializer_class


@extend_schema_view(
    list=extend_schema(
        responses=GrantCareerRepresentationSerializer(many=True)
    ),
    create=extend_schema(responses=GrantCareerRepresentationSerializer),
    retrieve=extend_schema(responses=GrantCareerRepresentationSerializer),
    update=extend_schema(responses=GrantCareerRepresentationSerializer),
    partial_update=extend_schema(responses=GrantCareerRepresentationSerializer),
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


@extend_schema_view(
    create=extend_schema(request=StudentCreateSerializer),
    update=extend_schema(request=StudentUpdateSerializer),
    partial_update=extend_schema(request=StudentUpdateSerializer),
)
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
        "user": ["isnull"],
        "user__id": ["exact"],
        "user__last_login": ["gte", "lte", "gt", "lt", "exact"],
        "user__is_superuser": ["exact"],
        "user__username": ["contains", "exact", "icontains", "search"],
        "user__email": ["contains", "exact", "icontains", "search"],
        "user__first_name": ["contains", "exact", "icontains", "search"],
        "user__last_name": ["contains", "exact", "icontains", "search"],
        "user__is_active": ["exact"],
        "user__is_staff": ["exact"],
        "user__groups__id": ["exact"],
        "user__groups__name": ["contains", "exact", "icontains", "search"],
    }
    search_fields = [
        "address",
        "registration_number",
        "first_name",
        "last_name",
        "user__username",
        "user__email",
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
        "user__username",
        "user__email",
    ]
    ordering = ["ci"]

    def get_serializer_class(self):
        if self.action == "create":
            return StudentCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return StudentUpdateSerializer
        return self.serializer_class


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
        "student": ["isnull"],
        "student__id": ["exact"],
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


@extend_schema_view(
    list=extend_schema(responses=SubjectRepresentationSerializer(many=True)),
    create=extend_schema(responses=SubjectRepresentationSerializer),
    retrieve=extend_schema(responses=SubjectRepresentationSerializer),
    update=extend_schema(responses=SubjectRepresentationSerializer),
    partial_update=extend_schema(responses=SubjectRepresentationSerializer),
)
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
        "student": ["isnull"],
        "student__id": ["exact"],
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
        "subject": ["isnull"],
        "subject__id": ["exact"],
        "subject__name": ["contains", "exact", "icontains", "search"],
        "subject__grade": ["exact"],
        "subject__tcp2_required": ["exact"],
        "school_year": ["isnull"],
        "school_year__id": ["exact"],
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


@extend_schema_view(
    list=extend_schema(
        responses=ApprovedSchoolCourseRepresentationSerializer(many=True)
    ),
    create=extend_schema(
        responses=ApprovedSchoolCourseRepresentationSerializer
    ),
    retrieve=extend_schema(
        responses=ApprovedSchoolCourseRepresentationSerializer
    ),
    update=extend_schema(
        responses=ApprovedSchoolCourseRepresentationSerializer
    ),
    partial_update=extend_schema(
        responses=ApprovedSchoolCourseRepresentationSerializer
    ),
)
class ApprovedSchoolCourseViewSet(BaseModelViewSet):
    queryset = ApprovedSchoolCourse.objects.all()
    serializer_class = ApprovedSchoolCourseSerializer

    filterset_fields = {
        "id": ["exact"],
        "date": ["gte", "lte", "gt", "lt", "exact"],
        "grade": ["gte", "lte", "gt", "lt", "exact"],
        "student": ["isnull"],
        "student__id": ["exact"],
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
        "school_year": ["isnull"],
        "school_year__id": ["exact"],
        "school_year__name": ["contains", "exact", "icontains", "search"],
        "school_year__start_date": ["gte", "lte", "gt", "lt", "exact"],
        "school_year__end_date": ["gte", "lte", "gt", "lt", "exact"],
    }
    search_fields = [
        "student__ci",
        "student__first_name",
        "student__last_name",
    ]
    ordering_fields = [
        "pk",
        "date",
        "grade",
        "school_year__start_date",
        "school_year__end_date",
        "student__ci",
        "student__first_name",
        "student__last_name",
    ]
    ordering = ["school_year__start_date"]


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
        try:
            if student.upgrading_7_8():
                serializer = self.get_serializer(student)
                return Response(serializer.data)
            return JsonResponse(
                {"error": "Tiene notas que no son validas"}, status=400
            )
        except serializers.ValidationError as e:
            return JsonResponse({"error": e.detail}, status=400)


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
    queryset = Student.get_students_current_9()
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

    def delete(self, request, *args, **kwargs):
        student: Student = self.get_object()
        StudentCareer.objects.filter(student=student).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BallotListView(BaseListAPIView):
    queryset = Student.get_students_current_9()
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        with_ballots = []
        for obj in queryset:
            if obj.has_ballot():
                with_ballots.append(obj)
        queryset = with_ballots
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class StudentsWithoutBallotsView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: StudentSerializer(many=True),
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            students = Student.get_students_without_ballots()
            return JsonResponse(
                StudentSerializer(students, many=True).data, safe=False
            )
        except serializers.ValidationError as e:
            return JsonResponse({"error": e.detail}, status=400)


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
            200: GrantCareerRepresentationSerializer(many=True),
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
            200: GrantCareerRepresentationSerializer(many=True),
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        grants = GrantCareer.current()
        return JsonResponse(
            GrantCareerSerializer(grants, many=True).data, safe=False
        )


class AreMissingBallotsView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: inline_serializer(
                "AreMissingBallots",
                fields={
                    "are_missing_ballots": serializers.BooleanField(
                        default=False
                    ),
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"are_missing_ballots": Student.are_missing_ballots()}
        )


class AreStudentsWhithoutRankingView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: inline_serializer(
                "AreStudentsWhithoutRanking",
                fields={
                    "are_students_whithout_ranking": serializers.BooleanField(
                        default=False
                    ),
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {
                "are_students_whithout_ranking": DegreeScale.there_are_students_whithout_ranking()
            }
        )


class UpgradingAllView(BaseModelAPIView):
    @extend_schema(
        responses={
            200: ApprovedSchoolCourseRepresentationSerializer(many=True),
            400: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            if Student.are_missing_ballots():
                return JsonResponse(
                    {"error": "Faltan estudiantes por boletas"}, status=400
                )
            if DegreeScale.there_are_students_whithout_ranking():
                return JsonResponse(
                    {
                        "error": "Faltan estudiantes por estar ubicados en el escalafon"
                    },
                    status=400,
                )
            GrantCareer.grant()
            Student.upgrading_7_8_all(grade=8)
            Student.upgrading_7_8_all(grade=7)
            approved_students = ApprovedSchoolCourse.objects.order_by(
                "grade", "student__ci"
            )
            return JsonResponse(
                ApprovedSchoolCourseRepresentationSerializer(
                    approved_students, many=True
                ).data,
                safe=False,
            )
        except serializers.ValidationError as e:
            return JsonResponse({"error": e.detail}, status=400)


class SubjectSectionCreateView(BaseModelAPIView):
    @extend_schema(
        request=SubjectSectionCreateSerializer(many=True),
        responses={
            200: inline_serializer(
                "SubjectSectionCreateResponse",
                fields={
                    "message": serializers.CharField(default="success"),
                },
            ),
            400: ErrorSerializer,
        },
    )
    def post(self, request, id, *args, **kwargs):
        subject = Subject.objects.filter(pk=id).first()
        course = SchoolYear.get_current_course()
        if not course:
            return JsonResponse(
                {"error": "No existe el curso escolar actual"}, status=400
            )
        if not subject:
            return JsonResponse(
                {"error": "No existe esta asignatura"}, status=400
            )
        serializer = SubjectSectionCreateSerializer(
            data=request.data, many=True
        )
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, safe=False, status=400)
        sections_ids = []
        for data_section in serializer.validated_data:
            section_index = data_section["index"]
            section_title = data_section["title"]
            section_description = data_section["description"]
            if "id" in data_section:
                section = data_section[
                    "id"
                ]  # SubjectSection.objects.get(id=data_section["id"])
                section.index = section_index
                section.title = section_title
                section.description = section_description
                section.save()
            else:
                section = SubjectSection.objects.create(
                    title=section_title,
                    description=section_description,
                    index=section_index,
                    subject=subject,
                    school_year=course,
                )
            sections_ids.append(section.id)
            folders_ids = []
            if "folders" in data_section:
                section_folders = data_section["folders"]
                for data_folder in section_folders:
                    folder_title = data_folder["title"]
                    folder_description = data_folder["description"]
                    if "id" in data_folder:
                        # folder_id = data_folder["id"]
                        folder = data_folder[
                            "id"
                        ]  # Folder.objects.get(id=folder_id)
                        folder.title = folder_title
                        folder.description = folder_description
                        folder.save()
                    else:
                        folder = Folder.objects.create(
                            title=folder_title,
                            description=folder_description,
                            subject_section=section,
                        )
                    folders_ids.append(folder.id)
                    folder_files_ids = []
                    if "files" in data_folder:
                        folder_files = data_folder["files"]

                        for data_file in folder_files:
                            file_title = data_file["title"]
                            file_description = data_file["description"]
                            file_file = data_file["file"]

                            if "id" in data_file:
                                # file = FileFolder.objects.get(
                                #     id=data_file["id"]
                                # )
                                file = data_file["id"]
                                file.title = file_title
                                file.description = file_description
                                file.type = get_extension(file_file)
                                file.file = file_file
                                file.folder = folder
                                file.save()
                            else:
                                file = FileFolder.objects.create(
                                    file=file_file,
                                    title=file_title,
                                    description=file_description,
                                    type=get_extension(file_file),
                                    folder=folder,
                                )
                            folder_files_ids.append(file.id)
                    FileFolder.objects.filter(folder=folder).exclude(
                        id__in=folders_ids
                    ).delete()
            Folder.objects.filter(subject_section=section).exclude(
                id__in=folders_ids
            ).delete()
            tasks_ids = []
            if "tasks" in data_section:
                section_tasks = data_section["tasks"]
                for data_task in section_tasks:
                    task_title = data_task["title"]
                    task_description = data_task["description"]

                    if "id" in data_task:
                        task = data_task[
                            "id"
                        ]  # SchoolTask.objects.get(id=data_task["id"])
                        task.title = task_title
                        task.description = task_description
                        task.subject_section = section
                        task.save()
                    else:
                        task = SchoolTask.objects.create(
                            title=task_title,
                            description=task_description,
                            subject_section=section,
                            date=timezone.now(),
                        )
                    tasks_ids.append(task.id)
                    task_file_ids = []
                    if "files" in data_task:
                        task_files = data_task["files"]

                        for data_task_file in task_files:
                            task_file_title = data_task_file["title"]
                            task_file_description = data_task_file[
                                "description"
                            ]
                            task_file_file = data_task_file["file"]

                            if "id" in data_task_file:
                                # file = FileSchoolTask.objects.get(
                                #     id=data_task_file["id"]
                                # )
                                file = data_task_file["id"]
                                file.title = task_file_title
                                file.description = task_file_description
                                file.type = get_extension(task_file_file)
                                file.file = task_file_file
                                file.school_task = task
                                file.save()
                            else:
                                file = FileSchoolTask.objects.create(
                                    file=task_file_file,
                                    title=task_file_title,
                                    description=task_file_description,
                                    type=get_extension(task_file_file),
                                    school_task=task,
                                )
                            task_file_ids.append(file.id)
                    FileSchoolTask.objects.filter(school_task=task).exclude(
                        id__in=task_file_ids
                    ).delete()
            SchoolTask.objects.filter(subject_section=section).exclude(
                id__in=tasks_ids
            ).delete()
        SubjectSection.objects.filter(subject=subject).exclude(
            id__in=sections_ids
        ).delete()
        return Response({"message": "success"}, status=200)

    @extend_schema(
        responses={
            200: SubjectSectionCreateRepresentationSerializer(many=True),
            400: ErrorSerializer,
        },
    )
    def get(self, request, id, *args, **kwargs):
        subject = Subject.objects.filter(pk=id).first()
        course = SchoolYear.get_current_course()
        if not course:
            return JsonResponse(
                {"error": "No existe el curso escolar actual"}, status=400
            )
        if not subject:
            return JsonResponse(
                {"error": "No existe esta asignatura"}, status=400
            )
        sections = SubjectSection.objects.filter(
            subject=subject, school_year=course
        ).order_by("index")
        return JsonResponse(
            SubjectSectionCreateRepresentationSerializer(
                sections, many=True, context={"request": request}
            ).data,
            safe=False,
            status=200,
        )


class SubjectOfUser(BaseModelAPIView):
    @extend_schema(
        responses={
            200: SubjectRepresentationSerializer(many=True),
            400: ErrorSerializer,
            403: ErrorSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name__in=[ROL_NAME_PROFESSOR]):
            professor = Professor.objects.filter(user=user).first()
            if professor:
                subjects = Subject.objects.filter(
                    professor__in=[professor]
                ).order_by("name")
                return JsonResponse(
                    SubjectRepresentationSerializer(subjects, many=True).data,
                    status=200,
                    safe=False,
                )

        elif user.groups.filter(name__in=[ROL_NAME_STUDENT]):
            student = Student.objects.filter(user=user).first()
            if student:
                subjects = Subject.objects.filter(grade=student.grade).order_by(
                    "name"
                )
                return JsonResponse(
                    SubjectRepresentationSerializer(subjects, many=True).data,
                    status=200,
                    safe=False,
                )
        elif user.groups.filter(name__in=[ROL_NAME_ADMIN]):
            subjects = Subject.objects.order_by("name")
            return JsonResponse(
                SubjectRepresentationSerializer(subjects, many=True).data,
                status=200,
                safe=False,
            )
        return JsonResponse({"error": "Usuario invalido"}, status=403)
