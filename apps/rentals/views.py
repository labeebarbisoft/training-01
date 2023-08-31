from django.views import View
from django.shortcuts import render, redirect
from .forms import (
    PickupDropoffLocationForm,
    VehicleSelectionForm,
    UserForm,
    ProfileForm,
    PickupDropoffDateTimeForm,
)
from .models import Vehicle, VehicleBookingRequest, Location
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class LocationList(LoginRequiredMixin, View):
    login_url = "/login"
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


class VehicleList(LoginRequiredMixin, View):
    login_url = "/login"
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


class UserRegister(LoginRequiredMixin, View):
    login_url = "/login"
    TEMPLATE = "rentals/register_user.html"
    USER_FORM = UserForm
    PROFILE_FORM = ProfileForm
    DATETIME_FORM = PickupDropoffDateTimeForm

    def get(self, request):
        user = request.user
        initial_user_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        initial_profile_data = {
            "contact_number": user.profile.contact_number,
        }

        user_form = self.USER_FORM(initial=initial_user_data)
        profile_form = self.PROFILE_FORM(initial=initial_profile_data)
        user_form.fields["username"].widget.attrs["readonly"] = True
        user_form.fields["email"].widget.attrs["readonly"] = True
        user_form.fields["first_name"].widget.attrs["readonly"] = True
        user_form.fields["last_name"].widget.attrs["readonly"] = True
        profile_form.fields["contact_number"].widget.attrs["readonly"] = True

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
        user = request.user
        if (
            user_form.is_valid()
            and profile_form.is_valid()
            and datetime_form.is_valid()
        ):
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
            return redirect("home")
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


class HomeView(LoginRequiredMixin, View):
    login_url = "/login"
    TEMPLATE = "rentals/home.html"

    def get(self, request):
        user = request.user
        booked_rides_model = user.profile.booked_rides.model
        field_names = [
            field.verbose_name.capitalize().replace("_", " ")
            for field in booked_rides_model._meta.get_fields()
        ]
        field_names.pop()
        context = {
            "field_names": field_names,
            "objs": user.profile.booked_rides.values,
        }
        return render(request, self.TEMPLATE, context)
