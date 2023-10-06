import graphene
from graphene_django import DjangoObjectType
from .models import Student, Branch, Subject
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "password")


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

    single_student = graphene.Field(StudentType, id=graphene.Int())

    def resolve_single_student(self, info, id):
        return Student.objects.get(pk=id)


class UserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, self, info, username, password):
        user = User(username=username, password=password)
        user.save()
        return UserMutation(user=user)


class Mutation(graphene.ObjectType):
    add_user = UserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
