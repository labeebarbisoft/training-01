from django.contrib import admin
from .models import (
    Vehicle,
    Profile,
    VehicleBookingRequest,
    User,
    VehicleCategory,
    Location,
    FareRate,
)


admin.site.register(Vehicle)
admin.site.register(Profile)
admin.site.register(VehicleBookingRequest)
admin.site.register(VehicleCategory)
admin.site.register(Location)
admin.site.register(FareRate)
admin.site.unregister(User)
admin.site.register(User)
