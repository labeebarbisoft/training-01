from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("selet_car", views.select_car, name="select_car"),
    path("register_user", views.register_user, name="register_user"),
]
