from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RideBookingForm
from .models import Car, Driver, RideRequest


def index(request):
    if request.method == "POST":
        form = RideBookingForm(request.POST)
        if form.is_valid():
            request.session["cleaned_data"] = request.POST
            return redirect("book_ride")
    else:
        form = RideBookingForm()
    return render(request, "rentals/index.html", {"form": form})


def book_ride(request):
    cleaned_data = request.session["cleaned_data"]
    pickup_location = cleaned_data["pickup_location"]
    dropoff_location = cleaned_data["dropoff_location"]
    selected_car_pk = cleaned_data["selected_car"]
    selected_driver_pk = cleaned_data["selected_driver"]

    selected_car = Car.objects.get(pk=selected_car_pk)
    selected_car.is_available = False
    selected_car.save()
    selected_driver = Driver.objects.get(pk=selected_driver_pk)
    selected_driver.is_available = False
    selected_driver.save()

    ride_request = RideRequest(
        pickup_location=pickup_location,
        dropoff_location=dropoff_location,
        car=selected_car,
        driver=selected_driver,
    )
    ride_request.save()
    return render(request, "rentals/success.html")
