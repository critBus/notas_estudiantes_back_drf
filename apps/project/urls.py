from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.project.views import (
    AwardViewSet,
    BallotCreateView,
    BallotListView,
    CareerViewSet,
    CurrentCurseView,
    DegreeScaleViewSet,
    DropoutViewSet,
    GraduationGradeViewSet,
    GraduationViewSet,
    SchoolYearViewSet,
    StudentCareerViewSet,
    StudentNoteViewSet,
    StudentViewSet,
    SubjectViewSet,
    Upgrading7and8,
)

router = DefaultRouter()

router.register(r"students", StudentViewSet)
router.register(r"dropouts", DropoutViewSet)
router.register(r"careers", CareerViewSet)
router.register(r"graduations", GraduationViewSet)
router.register(r"graduation_grades", GraduationGradeViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"student_note", StudentNoteViewSet)
router.register(r"awards", AwardViewSet)
router.register(r"student_careers", StudentCareerViewSet)
router.register(r"school_year", SchoolYearViewSet)
router.register(r"degree_scale", DegreeScaleViewSet)

urlpatterns = [
    path(
        "students/upgrading7and8/<int:id>/",
        Upgrading7and8.as_view(),
        name="upgrading7and8",
    ),
    path(
        "students/ballot/<int:id>/",
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
    path("", include(router.urls)),
]
