from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    School,
    City,
    Branch,
    Grade,
    Section,
    Subject,
    Attendance,
    Date,
    Student,
    Profile,
)
import base64
import json


class GraphQl(TestCase):
    def test_new_user_addition(self):
        graphql_query = """
                            mutation{
                                addUser(username:"ali", password:"123"){
                                    user{
                                        id
                                        username
                                    }
                                }
                            }
                        """
        expected_data = {"data": {"addUser": {"user": {"id": "1", "username": "ali"}}}}
        response = self.client.post("/graphql", {"query": graphql_query})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertJSONEqual(json.dumps(response_json), json.dumps(expected_data))
        profile = Profile.objects.get(pk=1)
        self.assertEqual(profile.role, "student")


# class Attendance401(TestCase):
#     def test_unauthorized_post_request(self):
#         url = reverse("attendance")
#         response = self.client.post(url, data={"key": "value"})
#         self.assertEqual(response.status_code, 401)


# class Attendance403(TestCase):
#     def setUp(self):
#         self.username = "testuser"
#         self.password = "testpassword"
#         self.user = User.objects.create_user(
#             username=self.username, password=self.password
#         )

#     def test_unauthorized_post_request(self):
#         url = reverse("attendance")
#         credentials = base64.b64encode(
#             f"{self.username}:{self.password}".encode()
#         ).decode()
#         response = self.client.post(
#             url,
#             HTTP_AUTHORIZATION=f"Basic {credentials}",
#         )
#         self.assertEqual(response.status_code, 403)


# class BaseTestCase(TestCase):
#     def setUp(self):
#         self.school = School.objects.create(pk=1, name="Arbisoft")
#         self.city = City.objects.create(pk=1, name="Lahore")
#         self.branch = Branch.objects.create(
#             pk=1,
#             name="Arbisoft",
#             address="25 Westwood Colony",
#             school=self.school,
#             city=self.city,
#         )
#         self.grade = Grade.objects.create(pk=1, name="10", branch=self.branch)
#         self.section = Section.objects.create(pk=1, name="A", grade=self.grade)
#         self.subject = Subject.objects.create(
#             pk=1, name="English", section=self.section
#         )
#         self.student = Student.objects.create(pk=1, name="Ali", branch=self.branch)
#         self.student.subjects.add(self.subject)
#         self.student.save()
#         self.date = Date.objects.create(date="2023-09-28")
#         self.attendance = Attendance.objects.create(
#             pk=1,
#             student=self.student,
#             subject=self.subject,
#             date=self.date,
#             status="absent",
#         )


# class GraphQl(BaseTestCase):
#     def setUp(self):
#         super().setUp()

#     def test_verify_returned_data(self):
#         graphql_query = """
#         query {
#             allStudents {
#                 id
#                 name
#             }
#         }
#         """
#         response = self.client.post("/graphql", {"query": graphql_query})
#         self.assertEqual(response.status_code, 200)
#         response_json = json.loads(response.content)
#         self.assertIn("data", response_json)
#         data = response_json["data"]
#         self.assertIn("allStudents", data)
#         students = data["allStudents"]
#         self.assertIsInstance(students, list)
#         self.assertTrue(len(students) > 0)
#         for student in students:
#             self.assertIn("id", student)
#             self.assertIn("name", student)


# class Attendance200(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.username = "superuser"
#         self.password = "superpassword"
#         self.superuser = User.objects.create_superuser(
#             username=self.username, password=self.password
#         )

#     def test_post_request_as_superuser(self):
#         url = reverse("attendance")
#         post_data = {"data": {"subject": 1, "date": "2023-09-28"}}
#         post_data = json.dumps(post_data)
#         credentials = base64.b64encode(
#             f"{self.username}:{self.password}".encode()
#         ).decode()
#         response = self.client.post(
#             url,
#             data=post_data,
#             content_type="application/json",
#             HTTP_AUTHORIZATION=f"Basic {credentials}",
#         )
#         self.assertEqual(response.status_code, 200)
