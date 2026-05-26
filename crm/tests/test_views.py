from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from crm.models import Client, Deal, Task, TaskComment


class ClientCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.manager = User.objects.create_user(
            username="test_manager_1",
            password="test-password",
            phone="+380995675128",
            position="Manager",
        )

    def setUp(self):
        self.client.force_login(self.manager)

    def test_client_manager_is_set_automatically(self):
        self.client.post(
            reverse("crm:client-create"),
            data={
                "first_name": "John",
                "phone": "+380995672361",
            },
        )

        created_client = Client.objects.get(phone="+380995672361")

        self.assertEqual(created_client.manager, self.manager)


class TaskCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.manager = User.objects.create_user(
            username="test_manager_1",
            password="test-password",
            phone="+380995675128",
            position="Manager",
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.manager,
        )

    def setUp(self):
        self.client.force_login(self.manager)

    def test_task_created_by_is_set_automatically(self):
        self.client.post(
            reverse("crm:task-create"),
            data={
                "title": "Test Task",
                "description": "Some description",
                "client": self.crm_client.pk,
                "assigned_to": self.manager.pk,
                "status": Task.Status.NEW,
                "priority": Task.Priority.MEDIUM,
                "due_date": str(date.today()),
            },
        )

        created_task = Task.objects.get(title="Test Task")

        self.assertEqual(created_task.created_by, self.manager)


class DealCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.manager = User.objects.create_user(
            username="deal_test_manager",
            password="test-password",
            phone="+380995675128",
            position="Manager",
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.manager,
        )

    def setUp(self):
        self.client.force_login(self.manager)

    def test_deal_manager_is_set_automatically(self):
        self.client.post(
            reverse("crm:deal-create"),
            data={
                "title": "Test Deal",
                "client": self.crm_client.pk,
                "amount": 100,
                "status": Deal.Status.NEW,
                "description": "Some description",
                "expected_close_date": str(date.today()),
            },
        )

        created_deal = Deal.objects.get(title="Test Deal")

        self.assertEqual(created_deal.manager, self.manager)


class TaskCommentCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.manager = User.objects.create_user(
            username="comment_test_manager",
            password="test-password",
            phone="+380995675128",
            position="Manager",
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.manager,
        )

        cls.task = Task.objects.create(
            title="Test Task",
            client=cls.crm_client,
            created_by=cls.manager,
            assigned_to=cls.manager,
            due_date=date.today(),
        )

    def setUp(self):
        self.client.force_login(self.manager)

    def test_comment_author_and_task_are_set_automatically(self):
        self.client.post(
            reverse("crm:task-comment-create", kwargs={"pk": self.task.pk}),
            data={
                "text": "Some comment text",
            },
        )

        created_comment = TaskComment.objects.get(text="Some comment text")

        self.assertEqual(created_comment.author, self.manager)
        self.assertEqual(created_comment.task, self.task)
