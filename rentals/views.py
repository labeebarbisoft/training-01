from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RideBookingForm


def index(request):
    if request.method == "POST":
        form = RideBookingForm(request.POST)
        if form.is_valid():
            request.session["cleaned_data"] = {"abc": "cde"}  # form.cleaned_data
            return redirect("book_ride")
    else:
        form = RideBookingForm()
    return render(request, "rentals/index.html", {"form": form})


def book_ride(request):
    cleaned_data = request.session["cleaned_data"]
    # pickup_location = cleaned_data["pickup_location"]
    # dropoff_location = cleaned_data["dropoff_location"]
    # selected_car = cleaned_data["selected_car"]
    # selected_driver = cleaned_data["selected_driver"]
    print(cleaned_data)
    return render(request, "rentals/success.html")
