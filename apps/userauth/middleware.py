from django.shortcuts import redirect
from django.http import Http404


# class PreventDriverLoginMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if (
#             request.path != "/login"
#             and request.user.is_authenticated
#             and request.user.profile.role == "driver"
#             and request.user.is_superuser is False
#         ):
#             raise Http404
#             return redirect("/logout")
#         return self.get_response(request)
