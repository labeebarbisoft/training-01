import json
from django.http import JsonResponse
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from .models import Drink
from .serializers import DrinkSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})


class DrinkList(View):
    def get(self, request):
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return JsonResponse({"drinks": serializer.data})

    def post(self, request):
        serializer = DrinkSerializer(data=json.loads(request.body.decode("utf-8")))
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
