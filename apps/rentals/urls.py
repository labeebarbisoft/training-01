from django.urls import path
from .views import (
    LocationList,
    VehicleList,
    UserRegister,
    HomeView,
    MessagesView,
    SubmitRating,
    MarkComplete,
    Extra,
    FileUpload,
    UserReports,
)
from . import views

urlpatterns = [
    path("", Extra.as_view(), name="extra"),
    path("book_ride/", LocationList.as_view(), name="location_menu"),
    path("vehicle_list/", VehicleList.as_view(), name="vehicle_menu"),
    path("register_user/", UserRegister.as_view(), name="register_user"),
    path("home/", HomeView.as_view(), name="home"),
    path("messages/", MessagesView.as_view(), name="messages"),
    path("submit_rating", SubmitRating.as_view(), name="submit_rating"),
    path("mark_complete", MarkComplete.as_view(), name="mark_complete"),
    path("file_upload/", FileUpload.as_view(), name="file_upload"),
    path("user_reports/", UserReports.as_view(), name="user_reports"),
]
