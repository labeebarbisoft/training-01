from django.contrib import admin
from .models import Car, CarDriver, RideRequest

admin.site.register(Car)
admin.site.register(CarDriver)
admin.site.register(RideRequest)
