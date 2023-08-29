from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserForm, ProfileForm
from django.contrib.auth import login, logout, authenticate
from apps.rentals.views import LocationList


class SignupView(View):
    TEMPLATE = "registration/signup.html"

    def get(self, request):
        return render(
            request,
            self.TEMPLATE,
            {
                "user_form": UserForm,
                "profile_form": ProfileForm,
            },
        )

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.user = user
            user.save()
            return redirect("login")
        return render(
            request,
            self.TEMPLATE,
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )
