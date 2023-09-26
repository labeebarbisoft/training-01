from rest_framework.views import APIView
from rest_framework.response import Response
from .models import City, School, Branch
from .serializers import BranchSerializer


class BranchView(APIView):
    def get(self, request):
        branch = Branch.objects.all()
        serializer = BranchSerializer(branch, many=True)
        return Response({"branch": serializer.data})
