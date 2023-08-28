from django.views import View
from django.shortcuts import render, redirect
from .forms import (
    PickupDropoffLocationForm,
    VehicleSelectionForm,
    UserForm,
    ProfileForm,
    PickupDropoffDateTimeForm,
)
from .models import Vehicle, Profile, VehicleBookingRequest, Location
from django.contrib.auth.models import User


class LocationList(View):
    TEMPLATE = "rentals/location_menu.html"
    LOCATION_FORM = PickupDropoffLocationForm

    def get(self, request):
        location_form = self.LOCATION_FORM()
        return render(request, self.TEMPLATE, {"form": location_form})

    def post(self, request):
        location_form = self.LOCATION_FORM(request.POST)
        if location_form.is_valid():
            request.session["pickup_location"] = location_form.cleaned_data[
                "pickup_location"
            ].pk
            request.session["dropoff_location"] = location_form.cleaned_data[
                "dropoff_location"
            ].pk
            return redirect("vehicle_menu")
        else:
            return render(request, self.TEMPLATE, {"form": location_form})


class VehicleList(View):
    TEMPLATE = "rentals/vehicle_menu.html"
    VEHICLE_FORM = VehicleSelectionForm

    def get(self, request):
        vehicle_form = self.VEHICLE_FORM()
        return render(
            request,
            self.TEMPLATE,
            {"form": vehicle_form},
        )

    def post(self, request):
        vehicle_form = self.VEHICLE_FORM(request.POST)
        if vehicle_form.is_valid():
            request.session["vehicle"] = vehicle_form.cleaned_data["selected_car"].pk
            return redirect("register_user")
        else:
            return render(request, self.TEMPLATE, {"form": vehicle_form})


class UserRegister(View):
    TEMPLATE = "rentals/register_user.html"
    USER_FORM = UserForm
    PROFILE_FORM = ProfileForm
    DATETIME_FORM = PickupDropoffDateTimeForm

    def get(self, request):
        user_form = self.USER_FORM()
        profile_form = self.PROFILE_FORM()
        datetime_form = self.DATETIME_FORM()
        return render(
            request,
            self.TEMPLATE,
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "pickup_dropoff_time_form": datetime_form,
            },
        )

    def post(self, request):
        user_form = self.USER_FORM(request.POST)
        profile_form = self.PROFILE_FORM(request.POST)
        datetime_form = self.DATETIME_FORM(request.POST)
        if (
            user_form.is_valid()
            and profile_form.is_valid()
            and datetime_form.is_valid()
        ):
            user = User(
                username=f"{request.POST['first_name']} {request.POST['last_name']}"
            )
            user.save()
            user.profile.role = "customer"
            user.profile.contact_number = "123"
            user.profile.save()
            ride_request = VehicleBookingRequest(
                pickup_location=Location.objects.get(
                    pk=request.session["pickup_location"]
                ),
                dropoff_location=Location.objects.get(
                    pk=request.session["dropoff_location"]
                ),
                pickup_datetime=datetime_form.cleaned_data["pickup_time"],
                status="pending",
                vehicle=Vehicle.objects.get(pk=request.session["vehicle"]),
                # driver=1,
                customer=user.profile,
            )
            ride_request.save()
            return render(request, "rentals/success.html")
        else:
            return render(
                request,
                self.TEMPLATE,
                {
                    "user_form": user_form,
                    "profile_form": profile_form,
                    "pickup_dropoff_time_form": datetime_form,
                },
            )
