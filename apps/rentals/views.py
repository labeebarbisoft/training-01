from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import (
    PickupDropoffLocationForm,
    VehicleSelectionForm,
    UserForm,
    ProfileForm,
    PickupDropoffDateTimeForm,
)
from .models import Vehicle, Profile, VehicleBookingRequest, User


class LocationList(View):
    template = "rentals/location_menu.html"
    form = PickupDropoffLocationForm

    def get(self, request):
        form = self.form()
        return render(request, self.template, {"form": form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            request.session["pickup_location"] = form.cleaned_data["pickup_location"]
            request.session["dropoff_location"] = form.cleaned_data["dropoff_location"]
            return redirect(
                "vehicle_menu"
            )  # Replace "select_car" with your actual URL name

        return render(request, self.template, {"form": form})


def select_car(request):
    if request.method == "POST":
        form = VehicleSelectionForm(request.POST)
        if form.is_valid():
            request.session["selected_car"] = request.POST["selected_car"]
            return redirect("register_user")
    else:
        form = VehicleSelectionForm()
    return render(request, "rentals/select_car.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        pickup_dropoff_time_form = PickupDropoffDateTimeForm(request.POST)
        if (
            user_form.is_valid()
            and profile_form.is_valid()
            and pickup_dropoff_time_form.is_valid()
        ):
            ride_req = VehicleBookingRequest(
                pickup_location=request.session["pickup_location"],
                dropoff_location=request.session["dropoff_location"],
                pickup_time=request.POST["pickup_time"],
                dropoff_time=request.POST["dropoff_time"],
            )
            ride_req.save()

            return render(request, "rentals/success.html")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        pickup_dropoff_time_form = PickupDropoffDateTimeForm()
    return render(
        request,
        "rentals/register_user.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "pickup_dropoff_time_form": pickup_dropoff_time_form,
        },
    )
