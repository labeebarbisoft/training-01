from django.contrib import admin
from .models import Car, Driver, RideRequest

admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(RideRequest)
