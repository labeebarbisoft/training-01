from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Driver(AbstractUser):
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Car(models.Model):
    FUEL_TYPES = [
        ("Gasoline", "Gasoline"),
        ("Diesel", "Diesel"),
    ]
    category = models.CharField(max_length=20)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    num_of_seats = models.IntegerField()
    fare_price_per_km = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category} {self.num_of_seats} Seater"


class RideRequest(models.Model):
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)

    driver_assigned = models.BooleanField(default=False, editable=False)
    car_assigned = models.BooleanField(default=False, editable=False)
    ride_completed = models.BooleanField(default=False)

    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ride_request_car",
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ride_request_driver",
    )

    def save(self, *args, **kwargs):
        if self.pk:
            ride_req_db = RideRequest.objects.get(pk=self.pk)
            if ride_req_db.ride_completed is True:
                raise ValidationError("Completed rides can not be edited.")

            if ride_req_db.driver is not None and self.driver != ride_req_db.driver:
                raise ValidationError("Assigned drivers can not be edited.")

            if ride_req_db.car is not None and self.car != ride_req_db.car:
                raise ValidationError("Assigned cars can not be edited.")

        if self.ride_completed is True:
            self.car.is_available = True
            self.car.save()
            self.driver.is_available = True
            self.driver.save()

        if (
            self.driver is not None
            and self.driver_assigned is False
            and self.ride_completed is False
        ):
            self.driver_assigned = True
            self.driver.is_available = False
            self.driver.save()
            print("here")

        if (
            self.car is not None
            and self.car_assigned is False
            and self.ride_completed is False
        ):
            self.car_assigned = True
            self.car.is_available = False
            self.car.save()
            print("here")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"From {self.pickup_location} to {self.dropoff_location} with {self.driver} on {self.car}"
