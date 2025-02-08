from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.project.views import (
    AwardViewSet,
    CareerViewSet,
    DropoutViewSet,
    GraduationGradeViewSet,
    GraduationViewSet,
    StudentCareerViewSet,
    StudentNoteViewSet,
    StudentViewSet,
    SubjectViewSet,
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

urlpatterns = [
    path("", include(router.urls)),
]
