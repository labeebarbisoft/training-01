from django.urls import path
from .views import LocationList
from . import views

urlpatterns = [
    path("", LocationList.as_view(), name="location_menu"),
    path("select_car", views.select_car, name="vehicle_menu"),
    path("register_user", views.register_user, name="user_ride_details_menu"),
]
