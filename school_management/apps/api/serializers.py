from rest_framework import serializers
from .models import City, School, Branch, Grade, Section, Attendance, Student, Subject


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "address", "school", "city"]


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ["id", "name", "branch"]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "name", "grade"]


class StudnetSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    branch = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ["id", "name", "branch", "subjects"]

    def get_subjects(self, obj):
        subjects_data = [
            {"id": subject.id, "name": subject.name} for subject in obj.subjects.all()
        ]
        return subjects_data


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()

    class Meta:
        model = Attendance
        fields = ["id", "student", "subject", "date", "status"]
