from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    Vehicle,
    Profile,
    VehicleBookingRequest,
    VehicleCategory,
    Location,
    FareRate,
)


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "get_user_is_active",
        "num_booking_requests",
        "num_ride_requests",
    ]
    list_filter = ["role", "user__date_joined"]

    @admin.display(boolean=True)
    def get_user_is_active(self, obj):
        return obj.user.is_active

    get_user_is_active.short_description = "User Is Active"

    def num_booking_requests(self, obj):
        if obj.role == "driver":
            return obj.drove_rides.count()
        else:
            return "N/A"

    num_booking_requests.short_description = "Number of Booking Requests"

    def num_ride_requests(self, obj):
        if obj.role == "customer":
            return obj.booked_rides.count()
        else:
            return "N/A"

    num_ride_requests.short_description = "Number of Ride Requests"


admin.site.register(Vehicle)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(VehicleBookingRequest)
admin.site.register(VehicleCategory)
admin.site.register(Location)
admin.site.register(FareRate)
admin.site.unregister(User)
admin.site.register(User)
