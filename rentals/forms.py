from django import forms
from .models import Profile, User, Car


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("contact_number",)


class PickupDropoffTimeForm(forms.Form):
    pickup_time = forms.DateTimeField(
        label="Pickup Location",
        required=True,
    )
    dropoff_location = forms.CharField(
        label="Dropoff Location",
        required=True,
    )


class PickupDropoffForm(forms.Form):
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


class CarSelectionForm(forms.Form):
    selected_car = forms.ModelChoiceField(
        label="Selected Car",
        queryset=Car.objects.all(),
        empty_label="Select vehicle",
    )
