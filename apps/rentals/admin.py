import csv
import logging
from itertools import product

from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import Http404

from .forms import FareRateCSVUploadForm
from .models import (
    FareRate,
    Location,
    StatusChangeNotification,
    Vehicle,
    VehicleBookingRequest,
    VehicleCategory,
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
    list_display = ("pickup_location", "dropoff_location", "vehicle", "status")
    list_filter = ("pickup_location", "dropoff_location", "vehicle")
    list_editable = ("status",)

    def save_model(self, request, obj, form, change):
        admin_user = request.user
        logger = logging.getLogger("change_logger")
        handler = logging.FileHandler("changes.log")
        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info(
            f"Admin {admin_user.username} changed the status of {obj} to {obj.status}"
        )
        try:
            super().save_model(request, obj, form, change)
        except Http404:
            messages.set_level(request, messages.ERROR)
            message = f"Invalid operation."
            messages.error(request, message)


@admin.register(FareRate)
class FareRateAdmin(admin.ModelAdmin):
    list_display = ("pickup", "dropoff", "vehicle", "fare")
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


class FareExportUtility:
    @staticmethod
    def export_fares(queryset):
        locations = Location.objects.values_list("id", flat=True)
        pickups = locations
        dropoffs = locations
        vehicle_ids = queryset.values_list("id", flat=True)

        combinations = product(pickups, dropoffs, vehicle_ids)

        data = []

        data.append(
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

        fare_rates = FareRate.objects.all().values(
            "pickup", "dropoff", "vehicle", "fare"
        )
        fare_rates_dict = {}
        for fare_rate in fare_rates:
            key = (fare_rate["pickup"], fare_rate["dropoff"], fare_rate["vehicle"])
            fare_rates_dict[key] = fare_rate["fare"]

        location_dict = {location.id: location for location in Location.objects.all()}
        vehicle_dict = {vehicle.id: vehicle for vehicle in Vehicle.objects.all()}

        for pickup, dropoff, vehicle in combinations:
            if pickup == dropoff:
                continue

            key = (pickup, dropoff, vehicle)
            fare = fare_rates_dict.get(key, 0)

            pickup_location = location_dict.get(pickup)
            dropoff_location = location_dict.get(dropoff)
            vehicle_used = vehicle_dict.get(vehicle)

            data.append(
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

        return data


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_filter = ("category",)
    list_display = ("category", "seating_capacity", "fuel_type", "is_active")
    list_editable = ("is_active",)

    actions = ["export_fares"]

    def export_fares(self, request, queryset):
        data = FareExportUtility.export_fares(queryset)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)

        for row in data:
            writer.writerow(row)

        return response

    export_fares.short_description = "Export Fares For Selected Vehicles"
