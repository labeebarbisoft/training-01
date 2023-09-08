from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import (
    Vehicle,
    VehicleBookingRequest,
    VehicleCategory,
    Location,
    FareRate,
    StatusChangeNotification,
)


admin.site.register(VehicleCategory)
admin.site.unregister(User)
admin.site.register(User)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("title", "full_address")


@admin.register(VehicleBookingRequest)
class VehicleBookingRequestAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            print("here")
            previous_instance = VehicleBookingRequest.objects.get(pk=obj.pk)

            valid = True
            if obj.status == previous_instance.status:
                pass
            elif previous_instance.status == "pending":
                if not (obj.status == "rejected" or obj.status == "approved"):
                    valid = False
            elif previous_instance.status == "approved":
                if not obj.status == "completed":
                    valid = False
            else:
                valid = False

            if valid is False:
                message = f"Invalid operation for object ID {obj.pk}."
                messages.error(request, message)
            else:
                super().save_model(request, obj, form, change)


@admin.register(FareRate)
class FareRateAdmin(admin.ModelAdmin):
    list_display = ("__str__", "fare")
    list_filter = ("pickup", "dropoff", "vehicle")
    list_editable = ("fare",)


@admin.register(StatusChangeNotification)
class StatusChangeNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "booking_request",
        "customer",
        "booking_status",
        "notification_status",
    )
    list_editable = ("notification_status",)
    list_filter = ("booking_status", "notification_status")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_filter = ("category",)
    list_display = ("__str__", "fuel_type", "is_active")
    list_editable = ("is_active",)
