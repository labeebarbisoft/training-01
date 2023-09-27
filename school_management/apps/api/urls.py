from django.urls import path
from .views import BranchView, GradeView, SectionView, AttendanceView

urlpatterns = [
    path("branch/", BranchView.as_view(), name="branch_view"),
    path("grade/", GradeView.as_view(), name="grade_view"),
    path("section/", SectionView.as_view(), name="section_view"),
    path("attendance/", AttendanceView.as_view(), name="attendance_view"),
]
