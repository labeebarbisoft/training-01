from django import forms
from .models import Profile, User, Vehicle, Location


class UserForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)


class ProfileForm(forms.Form):
    contact_number = forms.CharField(max_length=20, required=True)


class PickupDropoffDateTimeForm(forms.Form):
    pickup_time = forms.DateTimeField(
        label="Pickup Date/Time",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        required=True,
    )
    # dropoff_time = forms.DateTimeField(
    #     label="Dropoff Date/Time",
    #     widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    #     required=True,
    # )


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
    )
