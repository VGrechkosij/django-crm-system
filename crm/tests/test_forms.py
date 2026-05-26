from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase

from crm.models import Client, Task, Deal
from crm.forms.client_forms import ClientSearchForm
from crm.forms.deal_forms import DealSearchForm, DealForm
from crm.forms.task_forms import TaskForm, TaskSearchForm
from crm.forms.task_comment_forms import TaskCommentForm


class ClientSearchFormTest(TestCase):
    def test_search_form_valid_with_and_without_query(self):
        form_data = {"q": "test"}
        form_data_empty = {"q": ""}

        form = ClientSearchForm(data=form_data)
        form_empty = ClientSearchForm(data=form_data_empty)

        self.assertTrue(form.is_valid())
        self.assertTrue(form_empty.is_valid())


class DealSearchFormTest(TestCase):
    def test_search_form_valid_with_and_without_query(self):
        form_data = {"q": "test"}
        form_data_empty = {"q": ""}

        form = DealSearchForm(data=form_data)
        form_empty = DealSearchForm(data=form_data_empty)

        self.assertTrue(form.is_valid())
        self.assertTrue(form_empty.is_valid())


class TaskSearchFormTest(TestCase):
    def test_search_form_valid_with_and_without_query(self):
        form_data = {"q": "test"}
        form_data_empty = {"q": ""}

        form = TaskSearchForm(data=form_data)
        form_empty = TaskSearchForm(data=form_data_empty)

        self.assertTrue(form.is_valid())
        self.assertTrue(form_empty.is_valid())


class TaskFormTest(TestCase):
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

    def test_task_form_valid_with_correct_data(self):
        form_data = {
            "title": "test title",
            "description": "some description",
            "client": self.crm_client.pk,
            "assigned_to": self.user.pk,
            "status": Task.Status.NEW,
            "priority": Task.Priority.MEDIUM,
            "due_date": str(date.today()),
        }

        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_does_not_include_created_by(self):
        form = TaskForm()
        self.assertNotIn("created_by", form.fields)


class DealFormTest(TestCase):
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

    def test_deal_form_valid_with_correct_data(self):
        form_data = {
            "title": "test title",
            "client": self.crm_client.pk,
            "amount": 100,
            "status": Deal.Status.NEW,
            "description": "some description",
            "expected_close_date": str(date.today()),
        }

        form = DealForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_deal_form_does_not_include_manager(self):
        form = DealForm()
        self.assertNotIn("manager", form.fields)


class TaskCommentFormTest(TestCase):
    def test_comment_form_valid_with_text(self):
        form_data = {
            "text": "Some comment text",
        }

        form = TaskCommentForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_without_text(self):
        form_data = {
            "text": "",
        }

        form = TaskCommentForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_comment_form_has_only_text_field(self):
        form = TaskCommentForm()

        self.assertEqual(list(form.fields), ["text"])
