from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from crm.models import Client, Deal, Task, TaskComment


class ClientListPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.admin = User.objects.create_user(
            username="test_admin",
            password="test-password",
            phone="+380995675681",
            position="Admin",
            role=User.Role.ADMIN,
        )

        cls.manager_1 = User.objects.create_user(
            username="test_manager_1",
            password="test-password",
            phone="+380995675128",
            position="Manager",
        )

        cls.manager_2 = User.objects.create_user(
            username="test_manager_2",
            password="test-password",
            phone="+380995675836",
            position="Manager",
        )

        cls.support = User.objects.create_user(
            username="test_support",
            password="test-password",
            phone="+380995679360",
            position="Support",
            role=User.Role.SUPPORT,
        )

        cls.crm_client_1 = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.manager_1,
        )

        cls.crm_client_2 = Client.objects.create(
            first_name="Pitter",
            last_name="Tejo",
            phone="+380955675762",
            manager=cls.manager_2,
        )

    def test_admin_can_see_all_clients(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("crm:client-list"))
        clients = response.context["clients"]

        self.assertIn(self.crm_client_1, clients)
        self.assertIn(self.crm_client_2, clients)

    def test_manager_can_see_only_own_clients(self):
        self.client.force_login(self.manager_1)

        response = self.client.get(reverse("crm:client-list"))
        clients = response.context["clients"]

        self.assertIn(self.crm_client_1, clients)
        self.assertNotIn(self.crm_client_2, clients)

    def test_support_cannot_see_clients(self):
        self.client.force_login(self.support)

        response = self.client.get(reverse("crm:client-list"))
        clients = response.context["clients"]

        self.assertNotIn(self.crm_client_1, clients)
        self.assertNotIn(self.crm_client_2, clients)
        self.assertEqual(len(clients), 0)


class DealListPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.admin = User.objects.create_user(
            username="deal_test_admin",
            password="test-password",
            phone="+380995675681",
            position="Admin",
            role=User.Role.ADMIN,
        )

        cls.manager_1 = User.objects.create_user(
            username="deal_test_manager_1",
            password="test-password",
            phone="+380995675128",
            position="Manager",
        )

        cls.manager_2 = User.objects.create_user(
            username="deal_test_manager_2",
            password="test-password",
            phone="+380995675836",
            position="Manager",
        )

        cls.support = User.objects.create_user(
            username="deal_test_support",
            password="test-password",
            phone="+380995679360",
            position="Support",
            role=User.Role.SUPPORT,
        )

        cls.crm_client_1 = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.manager_1,
        )

        cls.crm_client_2 = Client.objects.create(
            first_name="Pitter",
            last_name="Tejo",
            phone="+380955675762",
            manager=cls.manager_2,
        )

        cls.deal_1 = Deal.objects.create(
            title="Deal 1",
            client=cls.crm_client_1,
            manager=cls.manager_1,
            amount=100,
            expected_close_date=date.today(),
        )

        cls.deal_2 = Deal.objects.create(
            title="Deal 2",
            client=cls.crm_client_2,
            manager=cls.manager_2,
            amount=200,
            expected_close_date=date.today(),
        )

    def test_admin_can_see_all_deals(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("crm:deal-list"))
        deals = response.context["deals"]

        self.assertIn(self.deal_1, deals)
        self.assertIn(self.deal_2, deals)

    def test_manager_can_see_only_own_deals(self):
        self.client.force_login(self.manager_1)

        response = self.client.get(reverse("crm:deal-list"))
        deals = response.context["deals"]

        self.assertIn(self.deal_1, deals)
        self.assertNotIn(self.deal_2, deals)

    def test_support_cannot_see_deals(self):
        self.client.force_login(self.support)

        response = self.client.get(reverse("crm:deal-list"))
        deals = response.context["deals"]

        self.assertNotIn(self.deal_1, deals)
        self.assertNotIn(self.deal_2, deals)
        self.assertEqual(len(deals), 0)


class TaskListPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.admin = User.objects.create_user(
            username="task_test_admin",
            password="test-password",
            phone="+380995675681",
            position="Admin",
            role=User.Role.ADMIN,
        )

        cls.manager_1 = User.objects.create_user(
            username="task_test_manager_1",
            password="test-password",
            phone="+380995675128",
            position="Manager",
        )

        cls.manager_2 = User.objects.create_user(
            username="task_test_manager_2",
            password="test-password",
            phone="+380995675836",
            position="Manager",
        )

        cls.support = User.objects.create_user(
            username="task_test_support",
            password="test-password",
            phone="+380995679360",
            position="Support",
            role=User.Role.SUPPORT,
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.manager_1,
        )

        cls.task_created_by_manager_1 = Task.objects.create(
            title="Task created by manager 1",
            client=cls.crm_client,
            created_by=cls.manager_1,
            assigned_to=cls.manager_2,
            due_date=date.today(),
        )

        cls.task_assigned_to_manager_1 = Task.objects.create(
            title="Task assigned to manager 1",
            client=cls.crm_client,
            created_by=cls.manager_2,
            assigned_to=cls.manager_1,
            due_date=date.today(),
        )

        cls.task_assigned_to_support = Task.objects.create(
            title="Task assigned to support",
            client=cls.crm_client,
            created_by=cls.manager_1,
            assigned_to=cls.support,
            due_date=date.today(),
        )

        cls.task_other_manager = Task.objects.create(
            title="Task other manager",
            client=cls.crm_client,
            created_by=cls.manager_2,
            assigned_to=cls.manager_2,
            due_date=date.today(),
        )

    def test_admin_can_see_all_tasks(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("crm:task-list"))
        tasks = response.context["tasks"]

        self.assertIn(self.task_created_by_manager_1, tasks)
        self.assertIn(self.task_assigned_to_manager_1, tasks)
        self.assertIn(self.task_assigned_to_support, tasks)
        self.assertIn(self.task_other_manager, tasks)

    def test_manager_can_see_created_or_assigned_tasks(self):
        self.client.force_login(self.manager_1)

        response = self.client.get(reverse("crm:task-list"))
        tasks = response.context["tasks"]

        self.assertIn(self.task_created_by_manager_1, tasks)
        self.assertIn(self.task_assigned_to_manager_1, tasks)
        self.assertIn(self.task_assigned_to_support, tasks)
        self.assertNotIn(self.task_other_manager, tasks)

    def test_support_can_see_only_assigned_tasks(self):
        self.client.force_login(self.support)

        response = self.client.get(reverse("crm:task-list"))
        tasks = response.context["tasks"]

        self.assertIn(self.task_assigned_to_support, tasks)
        self.assertNotIn(self.task_created_by_manager_1, tasks)
        self.assertNotIn(self.task_assigned_to_manager_1, tasks)
        self.assertNotIn(self.task_other_manager, tasks)


class CommentPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.admin = User.objects.create_user(
            username="comment_test_admin",
            password="test-password",
            phone="+380995675681",
            position="Admin",
            role=User.Role.ADMIN,
        )

        cls.author = User.objects.create_user(
            username="comment_test_author",
            password="test-password",
            phone="+380995675128",
            position="Manager",
        )

        cls.other_user = User.objects.create_user(
            username="comment_test_other_user",
            password="test-password",
            phone="+380995675836",
            position="Manager",
        )

        cls.crm_client = Client.objects.create(
            first_name="John",
            last_name="Smith",
            phone="+380995675561",
            manager=cls.author,
        )

        cls.task = Task.objects.create(
            title="Task created by author",
            client=cls.crm_client,
            created_by=cls.author,
            assigned_to=cls.other_user,
            due_date=date.today(),
        )

        cls.task_comment = TaskComment.objects.create(
            task=cls.task,
            author=cls.author,
            text="some text",
        )

    def test_admin_can_access_comment_update_page(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                "crm:task-comment-update",
                kwargs={"pk": self.task_comment.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_author_can_access_comment_update_page(self):
        self.client.force_login(self.author)

        response = self.client.get(
            reverse(
                "crm:task-comment-update",
                kwargs={"pk": self.task_comment.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_access_comment_update_page(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse(
                "crm:task-comment-update",
                kwargs={"pk": self.task_comment.pk}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_can_access_comment_delete_page(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                "crm:task-comment-delete",
                kwargs={"pk": self.task_comment.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_author_can_access_comment_delete_page(self):
        self.client.force_login(self.author)

        response = self.client.get(
            reverse(
                "crm:task-comment-delete",
                kwargs={"pk": self.task_comment.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_access_comment_delete_page(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse(
                "crm:task-comment-delete",
                kwargs={"pk": self.task_comment.pk}
            )
        )

        self.assertEqual(response.status_code, 404)
