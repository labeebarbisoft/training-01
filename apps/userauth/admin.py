from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "get_user_is_active",
        "num_driving_requests",
        "num_ride_requests",
    ]
    list_filter = ["role", "user__date_joined"]

    @admin.display(boolean=True)
    def get_user_is_active(self, obj):
        return obj.user.is_active

    get_user_is_active.short_description = "User Is Active"

    def num_driving_requests(self, obj):
        if obj.role == "driver":
            return obj.drove_rides.count()
        else:
            return "N/A"

    num_driving_requests.short_description = "Number of Driving Requests"

    def num_ride_requests(self, obj):
        if obj.role == "customer":
            return obj.booked_rides.count()
        else:
            return "N/A"

    num_ride_requests.short_description = "Number of Ride Requests"


admin.site.register(Profile, ProfileAdmin)
