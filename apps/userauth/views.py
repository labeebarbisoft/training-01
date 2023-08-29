from django.views import View
from django.shortcuts import render, redirect


class LoginView(View):
    TEMPLATE = "auth/login_menu.html"

    def get(self, request):
        return render(request, self.TEMPLATE)

    def post(self, request):
        return render(request, self.TEMPLATE)
