from django import forms

from crm.models import Task


class TaskSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search"})
    )


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
