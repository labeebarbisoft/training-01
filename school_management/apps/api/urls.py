from django.urls import path
from .views import (
    BranchView,
    GradeView,
    SectionView,
    CreateAttendanceView,
    GetAttendanceView,
    MarkAttendanceView,
    StudentInformationView,
)

urlpatterns = [
    path("branch/", BranchView.as_view(), name="branch"),
    path("grade/", GradeView.as_view(), name="grade"),
    path("section/", SectionView.as_view(), name="section"),
    path(
        "create_attendance/",
        CreateAttendanceView.as_view(),
        name="create_attendance",
    ),
    path(
        "get_attendance/",
        GetAttendanceView.as_view(),
        name="get_attendance",
    ),
    path(
        "mark_attendance/",
        MarkAttendanceView.as_view(),
        name="mark_attendance",
    ),
    path(
        "student_info/",
        StudentInformationView.as_view(),
        name="student_info",
    ),
]
