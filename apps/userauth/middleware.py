from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth import logout


class PreventDriverLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            # request.path != "/login"
            request.user.is_authenticated
            and request.user.profile.role == "driver"
            and request.user.is_superuser is False
        ):
            logout(request)
            return redirect("/login")
            raise Http404("You are not allowed to login")
        return self.get_response(request)
