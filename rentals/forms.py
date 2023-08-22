from django import forms
from .models import Car, Driver


class RideBookingForm(forms.Form):
    pickup_location = forms.CharField(
        label="Pickup Location",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter pickup location"}),
    )
    dropoff_location = forms.CharField(
        label="Dropoff Location",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter dropoff location"}),
    )
    selected_car = forms.ModelChoiceField(
        label="Selected Car",
        queryset=Car.objects.filter(is_available=True),
        empty_label="Select vehicle",
    )
    selected_driver = forms.ModelChoiceField(
        label="Selected Driver",
        queryset=Driver.objects.filter(is_available=True),
        empty_label="Select driver",
    )
