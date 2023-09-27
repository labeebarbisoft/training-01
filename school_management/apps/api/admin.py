from django.contrib import admin
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
