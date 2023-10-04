import graphene
from graphene_django import DjangoObjectType
from .models import Student, Branch, Subject

class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = ("id", "name", "branch", "subjects")

class BranchType(DjangoObjectType):
    class Meta:
        model = Branch
        fields = ("id", "name", "address")

class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject
        fields = ("id", "name")

class Query(graphene.ObjectType):
    all_students = graphene.List(StudentType)

    def resolve_all_students(self, info):
        return Student.objects.all()

schema = graphene.Schema(query=Query)