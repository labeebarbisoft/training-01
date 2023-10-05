import graphene
from graphene_django import DjangoObjectType, DjangoListField
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

    single_student = graphene.Field(StudentType, id=graphene.Int())

    def resolve_single_student(self, info, id):
        return Student.objects.get(pk=id)


class StudentMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        branch_id = graphene.Int(required=True)
        subject_ids = graphene.List(graphene.Int)

    student = graphene.Field(StudentType)

    @classmethod
    def mutate(cls, self, info, name, branch_id, subject_ids=None):
        branch = Branch.objects.get(pk=branch_id)
        if subject_ids is not None:
            subjects = Subject.objects.filter(pk__in=subject_ids)
        else:
            subjects = []

        student = Student(name=name, branch=branch)
        student.save()
        student.subjects.set(subjects)
        return StudentMutation(student=student)


class Mutation(graphene.ObjectType):
    add_student = StudentMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
