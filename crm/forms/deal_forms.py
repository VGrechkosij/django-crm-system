from django import forms

from crm.models import Deal


class DealSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={"placeholder": "Search"}
        )
    )


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = [
            "title",
            "client",
            "amount",
            "status",
            "description",
            "expected_close_date",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Description",
                    "rows": 4,
                }
            ),
            "expected_close_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            )
        }
