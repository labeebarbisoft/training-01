from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import base64
import json


class Attendance401(TestCase):
    def test_unauthorized_post_request(self):
        url = reverse("attendance")
        response = self.client.post(url, data={"key": "value"})
        self.assertEqual(response.status_code, 401)


class Attendance403(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_unauthorized_post_request(self):
        url = reverse("attendance")
        credentials = base64.b64encode(
            f"{self.username}:{self.password}".encode()
        ).decode()
        response = self.client.post(
            url,
            HTTP_AUTHORIZATION=f"Basic {credentials}",
        )
        self.assertEqual(response.status_code, 403)


# class Attendance200(TestCase):
#     def setUp(self):
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
#             body=post_data,
#             content_type="application/json",
#             HTTP_AUTHORIZATION=f"Basic {credentials}",
#         )
#         print(response.content.decode("utf-8"))
#         self.assertEqual(response.status_code, 200)
