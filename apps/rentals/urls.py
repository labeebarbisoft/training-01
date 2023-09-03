from django.urls import path
from .views import LocationList, VehicleList, UserRegister, HomeView, MessagesView
from . import views

urlpatterns = [
    path("", LocationList.as_view(), name="location_menu"),
    path("vehicle_list", VehicleList.as_view(), name="vehicle_menu"),
    path("register_user", UserRegister.as_view(), name="register_user"),
    path("home", HomeView.as_view(), name="home"),
    path("messages", MessagesView.as_view(), name="messages"),
]
