from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    PickupDropoffLocationForm,
    VehicleSelectionForm,
    UserForm,
    ProfileForm,
    PickupDropoffDateTimeForm,
)
from .models import Vehicle, VehicleBookingRequest, Location, FareRate


class BaseView(LoginRequiredMixin, View):
    login_url = "/login"


class LocationList(BaseView):
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
            return render(
                request,
                self.TEMPLATE,
                {"form": location_form},
            )


class VehicleList(BaseView):
    TEMPLATE = "rentals/vehicle_menu.html"
    VEHICLE_FORM = VehicleSelectionForm

    def get(self, request):
        vehicle_form = self.VEHICLE_FORM()
        fare_rates = FareRate.objects.active_fare_rates(
            pickup_location=request.session["pickup_location"],
            dropoff_location=request.session["dropoff_location"],
        )
        return render(
            request,
            self.TEMPLATE,
            {
                "form": vehicle_form,
                "fare_rates": fare_rates,
            },
        )

    def post(self, request):
        vehicle_form = self.VEHICLE_FORM(request.POST)
        if vehicle_form.is_valid():
            request.session["vehicle"] = vehicle_form.cleaned_data["selected_car"].pk
            return redirect("register_user")
        else:
            fare_rates = FareRate.objects.active_fare_rates(
                pickup_location=request.session["pickup_location"],
                dropoff_location=request.session["dropoff_location"],
            )
            return render(
                request,
                self.TEMPLATE,
                {
                    "form": vehicle_form,
                    "fare_rates": fare_rates,
                },
            )


class UserRegister(BaseView):
    TEMPLATE = "rentals/register_user.html"
    USER_FORM = UserForm
    PROFILE_FORM = ProfileForm
    DATETIME_FORM = PickupDropoffDateTimeForm

    def prepare_forms(self, request):
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

        return user_form, profile_form

    def get(self, request):
        user_form, profile_form = self.prepare_forms(request)
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
        user_form, profile_form = self.prepare_forms(request)
        datetime_form = self.DATETIME_FORM(request.POST)
        user = request.user
        if datetime_form.is_valid():
            ride_request = VehicleBookingRequest(
                pickup_location=Location.objects.get_by_id(
                    pk=request.session["pickup_location"]
                ),
                dropoff_location=Location.objects.get_by_id(
                    pk=request.session["dropoff_location"]
                ),
                pickup_datetime=datetime_form.cleaned_data["pickup_time"],
                status="pending",
                vehicle=Vehicle.objects.get_by_id(pk=request.session["vehicle"]),
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


class HomeView(BaseView):
    TEMPLATE = "rentals/home.html"

    def get(self, request):
        user = request.user
        field_names = ["ID", "Pickup", "Dropoff", "Time", "Status", "Vehicle", "Driver"]
        booked_rides = list(user.profile.booked_rides.all().order_by("-id"))
        context = {
            "field_names": field_names,
            "booked_rides": booked_rides,
        }
        return render(request, self.TEMPLATE, context)


class MessagesView(BaseView):
    TEMPLATE = "rentals/messages.html"

    def get(self, request):
        user = request.user
        notifications = list(user.profile.notifications.all().order_by("-id"))
        user.profile.notifications.filter(notification_status="delivered").update(
            notification_status="read"
        )
        return render(
            request,
            self.TEMPLATE,
            {"notifications": notifications},
        )


class SubmitRating(BaseView):
    TEMPLATE = "rentals/messages.html"

    def post(self, request):
        if not request.POST.get("rating") == "":
            booking_request_id = request.POST.get("booking_request_id")
            booking_request = VehicleBookingRequest.objects.get_by_id(
                pk=booking_request_id
            )
            booking_request.rating = request.POST.get("rating")
            booking_request.save()
            return redirect("messages")
        else:
            user = request.user
            notifications = list(user.profile.notifications.all().order_by("-id"))
            errors = ["Please select a rating before submitting."]
            return render(
                request,
                self.TEMPLATE,
                {
                    "errors": errors,
                    "notifications": notifications,
                },
            )


class MarkComplete(BaseView):
    def post(self, request):
        booking_request_id = request.POST.get("booking_request_id")
        booking_request = VehicleBookingRequest.objects.get_by_id(pk=booking_request_id)
        booking_request.status = "completed"
        booking_request.save()
        return redirect("messages")


class Extra(BaseView):
    def get(self, request):
        return redirect("home/")
