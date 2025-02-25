from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.project.views import (
    ApprovedSchoolCourseViewSet,
    AreMissingBallotsView,
    AreStudentsWhithoutRankingView,
    BallotCreateView,
    BallotListView,
    CareerViewSet,
    CarryOutGrantingOfCoursesView,
    CurrentCurseView,
    DegreeScaleCalculateView,
    DegreeScaleCurrentView,
    DegreeScaleViewSet,
    DropoutViewSet,
    FileFolderViewSet,
    FileSchoolTaskViewSet,
    FolderViewSet,
    GrantCareerCurrentView,
    GrantCareerViewSet,
    ProfessorViewSet,
    SchoolEventViewSet,
    SchoolTaskViewSet,
    SchoolYearViewSet,
    StudentCareerViewSet,
    StudentNoteViewSet,
    StudentResponseViewSet,
    StudentsWithoutBallotsView,
    StudentViewSet,
    SubjectSectionViewSet,
    SubjectViewSet,
    Upgrading7and8,
    UpgradingAllView,
)

router = DefaultRouter()

router.register(r"students", StudentViewSet, basename="students")
router.register(r"dropouts", DropoutViewSet)
router.register(r"careers", CareerViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"student_note", StudentNoteViewSet)
router.register(r"student_careers", StudentCareerViewSet)
router.register(r"school_year", SchoolYearViewSet)
router.register(r"degree_scale", DegreeScaleViewSet)
router.register(r"grant_career", GrantCareerViewSet)
router.register(r"approved_school_course", ApprovedSchoolCourseViewSet)
router.register(r"professor", ProfessorViewSet, basename="professor")
router.register(r"subject_section", SubjectSectionViewSet)
router.register(r"folder", FolderViewSet)
router.register(r"file_folder", FileFolderViewSet)
router.register(r"school_task", SchoolTaskViewSet)
router.register(r"file_school_task", FileSchoolTaskViewSet)
router.register(r"student_response", StudentResponseViewSet)
# router.register(r"professor_evaluation", ProfessorEvaluationViewSet)
router.register(r"school_event", SchoolEventViewSet)

urlpatterns = [
    path(
        "students/upgrading_all/",
        UpgradingAllView.as_view(),
        name="upgrading-all",
    ),
    path(
        "students/upgrading7and8/<int:pk>/",
        Upgrading7and8.as_view(),
        name="upgrading7and8",
    ),
    path(
        "students/ballot/are_missing/",
        AreMissingBallotsView.as_view(),
        name="ballot-are-missing",
    ),
    path(
        "students/ballot/without/",
        StudentsWithoutBallotsView.as_view(),
        name="ballot-are-without",
    ),
    path(
        "students/ballot/<int:pk>/",
        BallotCreateView.as_view(),
        name="create-ballot",
    ),
    path(
        "students/ballot/",
        BallotListView.as_view(),
        name="ballot-list",
    ),
    path(
        "school_year/current/",
        CurrentCurseView.as_view(),
        name="current-course",
    ),
    path(
        "degree_scale/calculated/",
        DegreeScaleCalculateView.as_view(),
        name="degree-scale-calculated",
    ),
    path(
        "degree_scale/current/",
        DegreeScaleCurrentView.as_view(),
        name="degree-scale-current",
    ),
    path(
        "degree_scale/exist_whithout/",
        AreStudentsWhithoutRankingView.as_view(),
        name="degree-scale-exist-whithout",
    ),
    path(
        "grant_career/current/",
        GrantCareerCurrentView.as_view(),
        name="grant-career-current",
    ),
    path(
        "grant_career/grant/",
        CarryOutGrantingOfCoursesView.as_view(),
        name="grant-career-grant",
    ),
    path("", include(router.urls)),
]
