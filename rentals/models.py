from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPES = [
        ("Customer", "Customer"),
        ("Driver", "Driver"),
    ]
    role = models.CharField(max_length=20, default="Customer", choices=USER_TYPES)
    contact_number = models.CharField(max_length=20)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField()
    ride_authorized = models.BooleanField(default=False)
    ride_completed = models.BooleanField(default=False)

    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ride_request_car",
    )
    driver = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ride_request_driver",
    )

    def __str__(self):
        return f"From {self.pickup_location} to {self.dropoff_location} with {self.driver} on {self.car}"
