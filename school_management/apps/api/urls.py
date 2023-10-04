from django.urls import path
from graphene_django.views import GraphQLView
from .views import (
    BranchView,
    GradeView,
    SectionView,
    CreateAttendanceView,
    AttendanceView,
    StudentInformationView,
    InformationView,
)
from .schema import schema

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
        "attendance/",
        AttendanceView.as_view(),
        name="attendance",
    ),
    path(
        "student_info/",
        StudentInformationView.as_view(),
        name="student_info",
    ),
    path(
        "information/",
        InformationView.as_view(),
        name="information",
    ),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
]
