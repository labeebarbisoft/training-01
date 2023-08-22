from django.contrib import admin
from .models import Car, Driver, RideRequest


class DriverModelAdmin(admin.ModelAdmin):
    exclude = (
        "last_login",
        "is_superuser",
        "groups",
        "user_permissions",
        "is_staff",
    )


admin.site.register(Car)
admin.site.register(Driver, DriverModelAdmin)
admin.site.register(RideRequest)
