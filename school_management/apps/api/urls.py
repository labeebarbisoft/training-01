from django.urls import path
from .views import BranchView

urlpatterns = [
    path("", BranchView.as_view(), name="branch_view"),
]
