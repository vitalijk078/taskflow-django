from django.test import Client, TestCase
from django.urls import reverse

from .models import Role, Task, User


class TaskFlowTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name=Role.USER)
        self.user = User.objects.create_user(username="student", password="password123", role=self.role)
        self.client = Client()

    def test_login_page_opens(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_task(self):
        self.client.login(username="student", password="password123")
        response = self.client.post(
            reverse("task_add"),
            {
                "title": "Подготовить отчет",
                "description": "Собрать материалы по практике",
                "status": Task.STATUS_NEW,
                "priority": Task.PRIORITY_HIGH,
                "due_date": "2030-01-01",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="Подготовить отчет", user=self.user).exists())
