from django import forms

from crm.models import TaskComment


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "placeholder": "Comment",
                    "rows": 4,
                }
            )
        }
