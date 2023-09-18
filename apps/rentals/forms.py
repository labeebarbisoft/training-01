from django import forms
from django.utils import timezone

from .models import Location, Vehicle


class FareRateCSVUploadForm(forms.Form):
    csv_file = forms.FileField()


class UserForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)


class ProfileForm(forms.Form):
    contact_number = forms.CharField(max_length=20, required=True)


class PickupDropoffDateForm(forms.Form):
    pickup_date = forms.DateField(
        label="Pickup Date",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        pickup_time = cleaned_data.get("pickup_time")
        now = timezone.now()

        if pickup_time and pickup_time <= now:
            self.add_error("pickup_time", "Pickup time must be in the future.")
        return cleaned_data


class PickupDropoffLocationForm(forms.Form):
    pickup_location = forms.ModelChoiceField(
        label="Pickup Location",
        queryset=Location.objects.all(),
        empty_label="Select pickup location",
    )
    dropoff_location = forms.ModelChoiceField(
        label="Dropoff Location",
        queryset=Location.objects.all(),
        empty_label="Select dropoff location",
    )

    def clean(self):
        cleaned_data = super().clean()
        pickup_location = cleaned_data.get("pickup_location")
        dropoff_location = cleaned_data.get("dropoff_location")

        if pickup_location and dropoff_location and pickup_location == dropoff_location:
            self.add_error(
                "pickup_location", "Pickup and dropoff locations cannot be the same."
            )

        return cleaned_data


class VehicleSelectionForm(forms.Form):
    selected_car = forms.ModelChoiceField(
        label="Selected Vehicle",
        queryset=Vehicle.objects.exclude(is_active=False),
        empty_label="Select vehicle",
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        selected_car = cleaned_data.get("selected_car")
        if not selected_car:
            self.add_error("selected_car", "Please select a vehicle.")
