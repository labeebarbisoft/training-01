import json
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import City, School, Branch
from .serializers import BranchSerializer


class BranchView(APIView):
    def get_branches(self):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return serializer.data

    def get(self, request):
        return Response({"Branches": self.get_branches()})

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        for item in data:
            serializer = BranchSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
        return Response({"Branches": self.get_branches()})

    def put(self, request):
        data = json.loads(request.body.decode("utf-8"))
        try:
            with transaction.atomic():
                for item in data:
                    branch = Branch.objects.get(id=item["id"])
                    serializer = BranchSerializer(branch, data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise AttributeError
                return Response(
                    {"message": "Branches updated successfully"},
                    status=status.HTTP_200_OK,
                )
        except Branch.DoesNotExist:
            return Response(
                {"message": "One or more branch ids do not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except KeyError:
            return Response(
                {"message": "Invalid field"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except AttributeError as e:
            return Response(
                {"message": "Invalid data in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
