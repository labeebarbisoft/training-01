from django import forms
from .models import Profile, User, Vehicle


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)


class ProfileForm(forms.Form):
    contact_number = forms.CharField(max_length=20, required=True)


class DateTimePickerInput(forms.DateTimeInput):
    input_type = "datetime-local"


class PickupDropoffDateTimeForm(forms.Form):
    pickup_time = forms.DateTimeField(
        label="Pickup Date/Time",
        widget=DateTimePickerInput,
        required=True,
    )
    dropoff_time = forms.DateTimeField(
        label="Dropoff Date/Time",
        widget=DateTimePickerInput,
        required=True,
    )


class PickupDropoffLocationForm(forms.Form):
    pickup_location = forms.CharField(
        label="Pickup Location",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter pickup location"}),
    )
    dropoff_location = forms.CharField(
        label="Dropoff Location",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter dropoff location"}),
    )


class VehicleSelectionForm(forms.Form):
    selected_car = forms.ModelChoiceField(
        label="Selected Car",
        queryset=Vehicle.objects.all(),
        empty_label="Select vehicle",
    )
