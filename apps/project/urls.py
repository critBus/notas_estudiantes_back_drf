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
    DegreeScaleCurrentReportView,
    DegreeScaleCurrentView,
    DegreeScaleViewSet,
    DropoutReportView,
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
    StudentGroupViewSet,
    StudentNoteMultipleCreateView,
    StudentNoteMultipleView,
    StudentNoteReportView,
    StudentNoteViewSet,
    StudentReportView,
    StudentResponseViewSet,
    StudentsWithoutBallotsView,
    StudentViewSet,
    SubjectOfUser,
    SubjectSectionCreateView,
    SubjectSectionStudentResponseOfUserView,
    SubjectSectionStudentResponseView,
    SubjectSectionTaskView,
    SubjectSectionViewSet,
    SubjectViewSet,
    Upgrading7and8,
    UpgradingAllView,
)

router = DefaultRouter()

router.register(r"students", StudentViewSet, basename="students")
router.register(r"dropouts", DropoutViewSet, basename="dropouts")
router.register(r"careers", CareerViewSet)
router.register(r"subjects", SubjectViewSet, basename="subjects")
router.register(r"student_note", StudentNoteViewSet, basename="student_note")
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
router.register(
    r"student_response", StudentResponseViewSet, basename="student_response"
)
# router.register(r"professor_evaluation", ProfessorEvaluationViewSet)
router.register(r"school_event", SchoolEventViewSet)
router.register(r"student_group", StudentGroupViewSet)

urlpatterns = [
    path(
        "students/report/",
        StudentReportView.as_view(),
        name="student-report",
    ),
    path(
        "dropouts/report/",
        DropoutReportView.as_view(),
        name="dropouts-report",
    ),
    path(
        "student_note/report/certification/<int:id_estudiante>/<int:grado>/",
        StudentNoteReportView.as_view(),
        name="student-note-certification-report",
    ),
    path(
        "student_note/report/subject/<int:pk>/",
        StudentNoteReportView.as_view(),
        name="student-note-subject-report",
    ),
    path(
        "student_note/multiple/",
        StudentNoteMultipleCreateView.as_view(),
        name="student-note-create-multiple",
    ),
    path(
        "student_note/multiple/<int:pk>/",
        StudentNoteMultipleView.as_view(),
        name="student-note-multiple",
    ),
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
        "degree_scale/report/",
        DegreeScaleCurrentReportView.as_view(),
        name="degree-scale-report",
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
    path(
        "subject_section/create/<int:id>/",
        SubjectSectionCreateView.as_view(),
        name="subject-section-create",
    ),
    path(
        "subject_section/subjects/",
        SubjectOfUser.as_view(),
        name="subject-section-subjects",
    ),
    path(
        "subject_section/tasks/<int:pk>/",
        SubjectSectionTaskView.as_view(),
        name="subject-section-taks",
    ),
    path(
        "subject_section/responses/<int:pk>/",
        SubjectSectionStudentResponseView.as_view(),
        name="subject-section-responses",
    ),
    path(
        "student_response/of_student/<int:pk>/",
        SubjectSectionStudentResponseOfUserView.as_view(),
        name="student-response-user",
    ),
    path("", include(router.urls)),
]
