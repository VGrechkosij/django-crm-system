from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from crm.models import (
    User,
    Client,
    Task,
    TaskComment,
    Deal,
)


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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "company",
        "manager",
        "created_at",
        "updated_at"
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "company",
        "manager__username",
        "manager__email",
    )

    list_filter = (
        "created_at",
        "updated_at",
        "manager"
    )

    ordering = (
        "-created_at",
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "assigned_to",
        "created_by",
        "status",
        "priority",
        "due_date",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "client__first_name",
        "client__last_name",
        "client__company",
        "assigned_to__username",
    )

    list_filter = (
        "status",
        "priority",
        "due_date",
        "assigned_to",
        "created_by",
        "client",
    )

    ordering = (
        "-due_date",
    )


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "author",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "task__title",
        "author__username",
    )

    list_filter = (
        "author",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "manager",
        "amount",
        "status",
        "expected_close_date",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "client__first_name",
        "client__last_name",
        "client__phone",
        "client__email",
        "client__company",
        "manager__username",
        "manager__email",
        "description",
    )

    list_filter = (
        "status",
        "expected_close_date",
        "created_at",
        "updated_at",
        "manager",
        "client",
    )

    ordering = (
        "-created_at",
    )
