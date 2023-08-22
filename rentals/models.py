from django.contrib.auth.models import AbstractUser
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

    STATUS_TYPES = [
        ("pending", "Pending Confirmation"),
        ("ongoing", "Ride In Progress"),
        ("finished", "Ride Completed"),
    ]
    current_status = models.CharField(
        max_length=20,
        choices=STATUS_TYPES,
        default="pending",
    )

    car = models.OneToOneField(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ride_request",
        limit_choices_to={"is_available": True},
    )
    driver = models.OneToOneField(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ride_request",
        limit_choices_to={"is_available": True},
    )

    def save(self, *args, **kwargs):
        if self.pk:
            if self.driver is not None and self.current_status == "ongoing":
                self.driver.is_available = False
                self.driver.save()
            if self.driver is not None and self.current_status == "finished":
                self.driver.is_available = True
                self.driver.save()

            if self.car is not None and self.current_status == "ongoing":
                self.car.is_available = False
                self.car.save()
            if self.car is not None and self.current_status == "finished":
                self.car.is_available = True
                self.car.save()
        else:
            if self.driver is not None:
                self.driver.is_available = False
                self.driver.save()
            if self.car is not None:
                self.car.is_available = False
                self.car.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"From {self.pickup_location} to {self.dropoff_location} with {self.driver} on {self.car}"
