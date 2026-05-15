from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "phone",
        "email",
        "first_name",
        "last_name",
        "position",
        "role",
        "is_staff",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "phone",
                    "position",
                    "role"
                )
            }
        ),
    )

    search_fields = (
        "username",
        "phone",
        "email",
        "first_name",
        "last_name",
        "position",
        "role",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "position",
        "role",
        "groups",
    )

    ordering = ("username",)
