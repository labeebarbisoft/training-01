from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from .models import (
    City,
    School,
    Branch,
    Grade,
    Section,
    Subject,
    Student,
    Date,
    Attendance,
    Profile,
)


admin.site.register(City)
admin.site.register(School)
admin.site.register(Branch)
admin.site.register(Grade)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Date)
admin.site.register(Attendance)
admin.site.register(Profile)
