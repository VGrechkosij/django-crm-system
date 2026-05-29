from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from crm.models import (
    Client,
    Task,
    TaskComment,
    Deal,
)


class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create_user(
            username="test",
            password="test-password",
            phone="+380995675681",
            position="Manager",
        )

    def test_custom_user_fields_and_str(self):
        self.assertEqual(str(self.user), "test")
        self.assertEqual(self.user.phone, "+380995675681")
        self.assertEqual(self.user.position, "Manager")
        self.assertEqual(self.user.role, self.user.Role.MANAGER)


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create_user(
            username="test",
            password="test-password",
            phone="+380995675681",
            position="Manager",
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.user,
        )

    def test_client_str(self):
        self.assertEqual(str(self.crm_client), "John Smith")

    def test_client_manager_related_name(self):
        self.assertIn(self.crm_client, self.user.clients.all())


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create_user(
            username="test",
            password="test-password",
            phone="+380995675681",
            position="Manager",
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.user,
        )

        cls.task = Task.objects.create(
            title="Call",
            client=cls.crm_client,
            created_by=cls.user,
            assigned_to=cls.user,
            due_date=date.today(),
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "Call")

    def test_task_related_names_and_defaults(self):
        self.assertIn(self.task, self.crm_client.tasks.all())
        self.assertIn(self.task, self.user.created_tasks.all())
        self.assertIn(self.task, self.user.assigned_tasks.all())
        self.assertEqual(self.task.status, self.task.Status.NEW)
        self.assertEqual(self.task.priority, self.task.Priority.MEDIUM)


class TaskCommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create_user(
            username="test",
            password="test-password",
            phone="+380995675681",
            position="Manager",
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.user,
        )

        cls.task = Task.objects.create(
            title="Call",
            client=cls.crm_client,
            created_by=cls.user,
            assigned_to=cls.user,
            due_date=date.today(),
        )

        cls.task_comment = TaskComment.objects.create(
            task=cls.task,
            author=cls.user,
            text="Some text",
        )

    def test_comment_str(self):
        self.assertEqual(str(self.task_comment), "Comment by test on Call")

    def test_comment_related_names(self):
        self.assertIn(self.task_comment, self.task.comments.all())
        self.assertIn(self.task_comment, self.user.task_comments.all())


class DealModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create_user(
            username="test",
            password="test-password",
            phone="+380995675681",
            position="Manager",
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.user,
        )

        cls.deal = Deal.objects.create(
            title="test deal",
            client=cls.crm_client,
            manager=cls.user,
            amount=100,
            expected_close_date=date.today(),
        )

    def test_deal_str(self):
        self.assertEqual(str(self.deal), "test deal")

    def test_deal_related_names_and_defaults(self):
        self.assertIn(self.deal, self.user.deals.all())
        self.assertIn(self.deal, self.crm_client.deals.all())
        self.assertEqual(self.deal.status, self.deal.Status.NEW)
