from django import forms


class ClientSearchForm(forms.Form):
    q = forms.CharField(
        max_length=255,
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name, email, phone, company, manager"
            }
        )
    )
