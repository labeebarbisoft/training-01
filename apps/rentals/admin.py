from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from import_export.admin import ExportActionMixin
from itertools import product
from django.http import HttpResponse
import csv
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
    search_fields = ("title",)


@admin.register(VehicleBookingRequest)
class VehicleBookingRequestAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status")
    list_filter = ("pickup_location", "dropoff_location", "vehicle")
    list_editable = ("status",)

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
                messages.set_level(request, messages.ERROR)
                message = f"Invalid operation for {obj}."
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
class VehicleAdmin(ExportActionMixin, admin.ModelAdmin):
    list_filter = ("category",)
    list_display = ("__str__", "fuel_type", "is_active")
    list_editable = ("is_active",)

    actions = ["export_fares"]

    def export_fares(self, request, queryset):
        pickups = Location.objects.values_list("id", flat=True)
        dropoffs = Location.objects.values_list("id", flat=True)
        vehicle_ids = queryset.values_list("id", flat=True)

        combinations = product(pickups, dropoffs, vehicle_ids)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)

        writer.writerow(
            [
                "pickup_id",
                "pickup",
                "dropoff_id",
                "dropoff",
                "vehicle_id",
                "vehicle",
                "fare",
            ]
        )

        for pickup, dropoff, vehicle in combinations:
            if pickup == dropoff:
                continue
            print(pickup, dropoff, vehicle)

            fare_rate = FareRate.objects.filter(
                pickup=pickup, dropoff=dropoff, vehicle=vehicle
            ).first()
            fare = fare_rate.fare if fare_rate else ""

            pickup_location = Location.objects.get(id=pickup)
            dropoff_location = Location.objects.get(id=dropoff)
            vehicle_used = Vehicle.objects.get(id=vehicle)

            writer.writerow(
                [
                    pickup,
                    pickup_location,
                    dropoff,
                    dropoff_location,
                    vehicle,
                    vehicle_used,
                    fare,
                ]
            )

        return response

    export_fares.short_description = "Export Fares For Selected Vehicles"
