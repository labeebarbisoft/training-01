""" Define model classes

This module contains Django modles for handling user authentication, 
defining entities and relationships between them.
"""


from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.userauth.models import Profile


class VehicleCategory(models.Model):
    category = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.category


class VehiclelManager(models.Manager):
    def get_by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            return None


class Vehicle(models.Model):
    category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE)
    FUEL_TYPES = [
        ("gasoline", "Gasoline"),
        ("diesel", "Diesel"),
    ]
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, blank=False)
    seating_capacity = models.IntegerField(blank=False)
    is_active = models.BooleanField(blank=False)
    image = models.ImageField(upload_to="images/", default=None)

    objects = VehiclelManager()

    def __str__(self):
        return f"{self.category} {self.seating_capacity} Seater"


class LocationlManager(models.Manager):
    def get_by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            return None


class Location(models.Model):
    title = models.CharField(max_length=20, blank=False)
    full_address = models.CharField(max_length=100, blank=False)

    objects = LocationlManager()

    def __str__(self):
        return self.title


class FareRateManager(models.Manager):
    def active_fare_rates(self, pickup_location, dropoff_location):
        return self.filter(
            pickup=pickup_location,
            dropoff=dropoff_location,
            vehicle__is_active=True,
        )


class FareRate(models.Model):
    pickup = models.ForeignKey(
        Location,
        related_name="pickup_fares",
        on_delete=models.CASCADE,
    )
    dropoff = models.ForeignKey(
        Location,
        related_name="dropoff_fares",
        on_delete=models.CASCADE,
    )
    vehicle = models.ForeignKey(
        Vehicle,
        related_name="vehicle_fares",
        on_delete=models.CASCADE,
    )
    fare = models.IntegerField(blank=False)

    objects = FareRateManager()

    def __str__(self):
        return f"{self.pickup} -> {self.dropoff} on {self.vehicle}"


class VehicleBookingRequestManager(models.Manager):
    def get_by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            return None


class VehicleBookingRequest(models.Model):
    pickup_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="pickups",
    )
    dropoff_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="dropoffs",
    )
    pickup_date = models.DateField(blank=False)
    STATUS_TYPES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_TYPES, blank=False)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        related_name="used_rides",
    )
    driver = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drove_rides",
    )
    customer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="booked_rides",
    )
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)], null=True, blank=True
    )
    fare = models.IntegerField()

    objects = VehicleBookingRequestManager()

    def __str__(self):
        return (
            f"From {self.pickup_location} to {self.dropoff_location} on {self.vehicle}"
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            previous_instance = VehicleBookingRequest.objects.get(pk=self.pk)

            if self.status != previous_instance.status:
                StatusChangeNotification.objects.create(
                    booking_request=self,
                    customer=self.customer,
                    booking_status=self.status,
                )
            super().save(*args, **kwargs)


class StatusChangeNotification(models.Model):
    booking_request = models.ForeignKey(
        VehicleBookingRequest,
        on_delete=models.CASCADE,
        related_name="status_changes",
    )
    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    BOOKING_STATUS_TYPES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_TYPES)
    NOTIFICATION_STATUS_TYPES = [
        ("pending", "Pending"),
        ("delivered", "Delivered"),
        ("read", "Read"),
    ]
    notification_status = models.CharField(
        max_length=20,
        choices=NOTIFICATION_STATUS_TYPES,
        default="delivered",
    )

    def __str__(self):
        return f"Ride: {self.booking_request} | Status: {dict(self.BOOKING_STATUS_TYPES)[self.booking_status]}"
