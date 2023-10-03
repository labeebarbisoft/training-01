from django.urls import path

from . import views
from .views import SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
