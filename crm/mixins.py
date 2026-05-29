from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == self.request.user.Role.ADMIN


class ClientPermissionMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == user.Role.MANAGER:
            queryset = queryset.filter(manager=user)

        elif user.role != user.Role.ADMIN:
            queryset = queryset.none()

        return queryset


class TaskPermissionMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == user.Role.ADMIN:
            return queryset

        if user.role == user.Role.MANAGER:
            return queryset.filter(
                Q(created_by=user) | Q(assigned_to=user)
            )

        if user.role == user.Role.SUPPORT:
            return queryset.filter(assigned_to=user)

        return queryset.none()


class DealPermissionMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == user.Role.MANAGER:
            queryset = queryset.filter(manager=user)

        elif user.role != user.Role.ADMIN:
            queryset = queryset.none()

        return queryset


class CommentPermissionMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == user.Role.ADMIN:
            return queryset

        return queryset.filter(author=user)
