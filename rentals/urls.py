from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("book_ride", views.book_ride, name="book_ride"),
]
