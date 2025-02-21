from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.project.views import (
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
    GrantCareerCurrentView,
    GrantCareerViewSet,
    SchoolYearViewSet,
    StudentCareerViewSet,
    StudentNoteViewSet,
    StudentsWithoutBallotsView,
    StudentViewSet,
    SubjectViewSet,
    Upgrading7and8,
)

router = DefaultRouter()

router.register(r"students", StudentViewSet)
router.register(r"dropouts", DropoutViewSet)
router.register(r"careers", CareerViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"student_note", StudentNoteViewSet)
router.register(r"student_careers", StudentCareerViewSet)
router.register(r"school_year", SchoolYearViewSet)
router.register(r"degree_scale", DegreeScaleViewSet)
router.register(r"grant_career", GrantCareerViewSet)

urlpatterns = [
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
