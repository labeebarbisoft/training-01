from django.contrib.auth.models import AbstractUser
from django.db import models


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)


class CarDriver(AbstractUser):
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Car(models.Model):
    FUEL_TYPES = [
        ("Gasoline", "Gasoline"),
        ("Diesel", "Diesel"),
    ]
    category = models.CharField(max_length=50, null=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    num_of_seats = models.IntegerField(default=0)
    fare_price_per_km = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    driver = models.OneToOneField(
        CarDriver,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return f"{self.category} {self.num_of_seats} Seater"


class RideRequest(models.Model):
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    car = models.OneToOneField(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ride_request",
        limit_choices_to={"is_available": True},
    )
    driver = models.OneToOneField(
        CarDriver,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ride_request",
        limit_choices_to={"is_available": True},
    )

    def __str__(self):
        return f"From {self.pickup_location} to {self.dropoff_location} with {self.driver} on {self.car}"
