import json
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Drink
from .serializers import DrinkSerializer
from django.http import JsonResponse


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class DrinkList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return JsonResponse({"drinks": serializer.data})

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        for item in data:
            serializer = DrinkSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"data": serializer.data}, status=status.HTTP_201_CREATED
                )
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = json.loads(request.body.decode("utf-8"))
        for item in data:
            drink = Drink.objects.get(id=item["id"])
            serializer = DrinkSerializer(drink, data=item)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
