import json
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import City, School, Branch, Grade, Section, Subject, Attendance, Date
from .serializers import BranchSerializer, GradeSerializer, SectionSerializer


class BranchView(APIView):
    def get_branches(self):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return serializer.data

    def get(self, request):
        return Response(
            {"Branches": self.get_branches()},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        try:
            with transaction.atomic():
                for item in data:
                    serializer = BranchSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise KeyError
                return Response(
                    {
                        "message": "Branches added successfully",
                        "Branches": self.get_branches(),
                    },
                    status.HTTP_200_OK,
                )
        except KeyError:
            return Response(
                {"message": "Invalid data in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
                        raise KeyError
                return Response(
                    {
                        "message": "Branches updated successfully",
                        "Branches": self.get_branches(),
                    },
                    status=status.HTTP_200_OK,
                )
        except Branch.DoesNotExist:
            return Response(
                {"message": "One or more branch ids do not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except KeyError:
            return Response(
                {"message": "Invalid data in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GradeView(APIView):
    def get_grades(self):
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return serializer.data

    def get(self, request):
        return Response(
            {"Grades": self.get_grades()},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        try:
            with transaction.atomic():
                for item in data:
                    serializer = GradeSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise KeyError
                return Response(
                    {
                        "message": "Grades added successfully",
                        "Grades": self.get_grades(),
                    },
                    status.HTTP_200_OK,
                )
        except KeyError:
            return Response(
                {"message": "Invalid data in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        data = json.loads(request.body.decode("utf-8"))
        try:
            with transaction.atomic():
                for item in data:
                    grade = Grade.objects.get(id=item["id"])
                    serializer = GradeSerializer(grade, data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise KeyError
                return Response(
                    {
                        "message": "Grades updated successfully",
                        "Grades": self.get_grades(),
                    },
                    status=status.HTTP_200_OK,
                )
        except Branch.DoesNotExist:
            return Response(
                {"message": "One or more grades ids do not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except KeyError:
            return Response(
                {"message": "Invalid data in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SectionView(APIView):
    def get_sections(self):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return serializer.data

    def get(self, request):
        return Response(
            {"Sections": self.get_sections()},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        try:
            with transaction.atomic():
                for item in data:
                    serializer = SectionSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise KeyError
                return Response(
                    {
                        "message": "Sections added successfully",
                        "Sections": self.get_sections(),
                    },
                    status.HTTP_200_OK,
                )
        except KeyError:
            return Response(
                {"message": "Invalid data in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        data = json.loads(request.body.decode("utf-8"))
        try:
            with transaction.atomic():
                for item in data:
                    section = Section.objects.get(id=item["id"])
                    serializer = SectionSerializer(section, data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise KeyError
                return Response(
                    {
                        "message": "Sections updated successfully",
                        "Sections": self.get_sections(),
                    },
                    status=status.HTTP_200_OK,
                )
        except Branch.DoesNotExist:
            return Response(
                {"message": "One or more sections ids do not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except KeyError:
            return Response(
                {"message": "Invalid data in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AttendanceView(APIView):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        for item in data:
            subject_id = item["subject"]
            date_id = item["date"]
            subject = Subject.objects.get(pk=subject_id)
            date = Date.objects.get(date=date_id)
            enrolled_students = subject.student_set.all()
            for student in enrolled_students:
                Attendance.objects.create(
                    student=student,
                    subject=subject,
                    date=date,
                )
        return Response(
            {"message": "Attendance added successfully"},
            status.HTTP_200_OK,
        )
