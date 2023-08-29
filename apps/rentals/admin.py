from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    Vehicle,
    VehicleBookingRequest,
    VehicleCategory,
    Location,
    FareRate,
)


admin.site.register(Vehicle)
admin.site.register(VehicleBookingRequest)
admin.site.register(VehicleCategory)
admin.site.register(Location)
admin.site.register(FareRate)
admin.site.unregister(User)
admin.site.register(User)
