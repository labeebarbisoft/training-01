from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import (
    PickupDropoffForm,
    CarSelectionForm,
    UserForm,
    ProfileForm,
    PickupDropoffTimeForm,
)
from .models import Car, Profile, RideRequest


def index(request):
    if request.method == "POST":
        form = PickupDropoffForm(request.POST)
        if form.is_valid():
            request.session["pickup_location"] = request.POST["pickup_location"]
            request.session["dropoff_location"] = request.POST["dropoff_location"]
            return redirect("select_car")
    else:
        form = PickupDropoffForm()
    return render(request, "rentals/index.html", {"form": form})


def select_car(request):
    if request.method == "POST":
        form = CarSelectionForm(request.POST)
        if form.is_valid():
            request.session["selected_car"] = request.POST["selected_car"]
            return redirect("register_user")
    else:
        form = CarSelectionForm()
    return render(request, "rentals/select_car.html", {"form": form})


#     pickup_location = request.session["pickup_location"]
#     dropoff_location = request.session["dropoff_location"]
#     selected_car = request.session["selected_car"]


def register_user(request):
    print("here")
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        pickup_dropoff_time_form = PickupDropoffTimeForm(request.POST)
        if (
            user_form.is_valid()
            and profile_form.is_valid()
            and pickup_dropoff_time_form.is_valid()
        ):
            user_form.save()
            profile_form.save()
            messages.success(request, _("Your profile was successfully updated!"))
            return redirect("add_to_db")
        else:
            messages.error(request, _("Please correct the error below."))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        pickup_dropoff_time_form = PickupDropoffTimeForm()
    return render(
        request,
        "rentals/register_user.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "pickup_dropoff_time_form": pickup_dropoff_time_form,
        },
    )


def add_to_db(request):
    pass
