from django import forms
from django.contrib.auth import get_user_model

from crm.models import Task


User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "client",
            "assigned_to",
            "status",
            "priority",
            "due_date",
        ]
        widgets = {
            "due_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }


class TaskSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search"})
    )


class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[("", "All statuses")] + list(Task.Status.choices),
        required=False,
    )
    priority = forms.ChoiceField(
        choices=[("", "All priorities")] + list(Task.Priority.choices),
        required=False
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label="All assignees",
    )
