""" Define model classes

This module contains Django modles for handling user authentication 
and defining relationships between database tables.
"""


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_TYPES = [
        ("customer", "Customer"),
        ("driver", "Driver"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_TYPES, blank=False)
    contact_number = models.CharField(max_length=20, blank=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class VehicleCategory(models.Model):
    VEHICLE_CATEGORY_TYPES = [
        ("sedan", "Sedan"),
        ("coaster", "Coaster"),
        ("grand_cabin", "Grand Cabin"),
    ]
    category = models.CharField(
        max_length=20,
        choices=VEHICLE_CATEGORY_TYPES,
        blank=False,
    )

    def __str__(self):
        return dict(self.VEHICLE_CATEGORY_TYPES)[self.category]


class Vehicle(models.Model):
    category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE)
    FUEL_TYPES = [
        ("gasoline", "Gasoline"),
        ("diesel", "Diesel"),
    ]
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, blank=False)
    seating_capacity = models.IntegerField(blank=False)
    is_active = models.BooleanField(blank=False)

    def __str__(self):
        return f"{self.category} {self.seating_capacity} Seater"


class Location(models.Model):
    title = models.CharField(max_length=20, blank=False)
    full_address = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.title


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
    fare = models.IntegerField(blank=False)

    def __str__(self):
        return f"{self.pickup} -> {self.dropoff} | Fare: {self.fare}"


@receiver(post_save, sender=Location)
def create_fare_entries(sender, instance, created, **kwargs):
    if created:
        all_locations = Location.objects.exclude(pk=instance.pk)
        for other_location in all_locations:
            FareRate.objects.create(
                pickup=instance,
                dropoff=other_location,
                fare=len(str(other_location)) + len(str(instance)),
            )
            FareRate.objects.create(
                pickup=other_location,
                dropoff=instance,
                fare=len(str(other_location)) + len(str(instance)),
            )


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
    pickup_datetime = models.DateTimeField(blank=False)
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

    def __str__(self):
        return f"From {self.pickup_location} to {self.dropoff_location} with {self.driver} on {self.vehicle}"
