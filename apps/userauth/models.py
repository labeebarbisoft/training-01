from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProfileManager(models.Manager):
    def get_orders(self, profile):
        return self.filter(pk=profile.pk).aggregate(total_orders=Count("booked_rides"))

    def get_fares(self, profile):
        return self.filter(pk=profile.pk).aggregate(
            total_fare=Sum("booked_rides__fare")
        )

    def get_reports_for_all_profiles(self):
        return (
            self.filter(role="customer")
            .annotate(
                total_rides=Count("booked_rides"),
                total_fare=Coalesce(Sum("booked_rides__fare"), 0),
            )
            .values("user__username", "total_rides", "total_fare")
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_TYPES = [
        ("customer", "Customer"),
        ("driver", "Driver"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_TYPES, blank=False)
    contact_number = models.CharField(max_length=20, blank=False)

    objects = ProfileManager()

    def unread_notification_count(self):
        return self.notifications.exclude(notification_status="read").count()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role="customer")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
