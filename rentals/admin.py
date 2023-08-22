from django.contrib import admin
from .models import Car, Driver, RideRequest


class RideRequestModelAdmin(admin.ModelAdmin):
    exclude = ("current_status",)


admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(RideRequest, RideRequestModelAdmin)
