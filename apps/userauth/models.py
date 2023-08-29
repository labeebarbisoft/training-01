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

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.username.endswith("Cust"):
            Profile.objects.create(user=instance, role="customer")
        else:
            Profile.objects.create(user=instance, role="driver")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
