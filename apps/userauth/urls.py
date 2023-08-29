from django.urls import path
from .views import SignupView
from . import views

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
]
