from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views.generic import (
    FormView,
    TemplateView,
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms.client_forms import ClientSearchForm
from .forms.task_forms import TaskForm, TaskSearchForm, TaskFilterForm
from .forms.task_comment_forms import TaskCommentForm
from .forms.deal_forms import DealSearchForm, DealForm
from .models import Client, Task, Deal, TaskComment
from .mixins import (
    ClientPermissionMixin,
    TaskPermissionMixin,
    DealPermissionMixin,
    AdminRequiredMixin,
    CommentPermissionMixin,
)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "crm/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["clients_count"] = Client.objects.count()
        context["tasks_count"] = Task.objects.count()
        context["deals_count"] = Deal.objects.count()

        context["open_tasks_count"] = Task.objects.exclude(
            status=Task.Status.DONE
        ).count()

        context["won_deals_count"] = Deal.objects.filter(
            status=Deal.Status.WON
        ).count()

        return context


class ClientListView(LoginRequiredMixin, ClientPermissionMixin, ListView):
    model = Client
    template_name = "crm/clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ClientSearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data["q"]
            if query:
                queryset = queryset.filter(
                    Q(first_name__icontains=query)
                    | Q(last_name__icontains=query)
                    | Q(email__icontains=query)
                    | Q(phone__icontains=query)
                    | Q(company__icontains=query)
                    | Q(manager__username__icontains=query)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = ClientSearchForm(self.request.GET)

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()

        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = "crm/clients/client_form.html"
    context_object_name = "client"
    fields = ["first_name", "last_name", "email", "phone", "company"]
    success_url = reverse_lazy("crm:client-list")

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, ClientPermissionMixin, DetailView):
    model = Client
    template_name = "crm/clients/client_detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.tasks.all()
        context["deals"] = self.object.deals.all()

        return context


class ClientUpdateView(LoginRequiredMixin, ClientPermissionMixin, UpdateView):
    model = Client
    template_name = "crm/clients/client_form.html"
    context_object_name = "client"
    fields = ["first_name", "last_name", "email", "phone", "company"]
    success_url = reverse_lazy("crm:client-list")


class ClientDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Client
    template_name = "crm/clients/client_confirm_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("crm:client-list")


class TaskListView(LoginRequiredMixin, TaskPermissionMixin, ListView):
    model = Task
    template_name = "crm/tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_form = TaskSearchForm(self.request.GET)
        filter_form = TaskFilterForm(self.request.GET)

        if search_form.is_valid():
            query = search_form.cleaned_data["q"]

            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query)
                    | Q(client__first_name__icontains=query)
                    | Q(client__last_name__icontains=query)
                )

        if filter_form.is_valid():
            status = filter_form.cleaned_data["status"]
            priority = filter_form.cleaned_data["priority"]
            assigned_to = filter_form.cleaned_data["assigned_to"]

            if status:
                queryset = queryset.filter(status=status)

            if priority:
                queryset = queryset.filter(priority=priority)

            if assigned_to:
                queryset = queryset.filter(assigned_to=assigned_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET)
        context["filter_form"] = TaskFilterForm(self.request.GET)

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "crm/tasks/task_form.html"
    context_object_name = "task"
    form_class = TaskForm
    success_url = reverse_lazy("crm:task-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, TaskPermissionMixin, DetailView):
    model = Task
    template_name = "crm/tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = TaskCommentForm()
        return context


class TaskUpdateView(LoginRequiredMixin, TaskPermissionMixin, UpdateView):
    model = Task
    template_name = "crm/tasks/task_form.html"
    context_object_name = "task"
    form_class = TaskForm
    success_url = reverse_lazy("crm:task-list")


class TaskDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Task
    template_name = "crm/tasks/task_confirm_delete.html"
    context_object_name = "task"
    success_url = reverse_lazy("crm:task-list")


class TaskCommentCreateView(LoginRequiredMixin, FormView):
    form_class = TaskCommentForm

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.task = self.task
        comment.author = self.request.user
        comment.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("crm:task-detail", kwargs={"pk": self.task.pk})


class TaskCommentUpdateView(LoginRequiredMixin, CommentPermissionMixin, UpdateView):
    model = TaskComment
    form_class = TaskCommentForm
    template_name = "crm/tasks/comment_form.html"
    context_object_name = "task_comment"

    def get_success_url(self):
        return reverse("crm:task-detail",  kwargs={"pk": self.object.task.pk})


class TaskCommentDeleteView(LoginRequiredMixin, CommentPermissionMixin, DeleteView):
    model = TaskComment
    template_name = "crm/tasks/comment_confirm_delete.html"
    context_object_name = "task_comment"

    def get_success_url(self):
        return reverse("crm:task-detail",  kwargs={"pk": self.object.task.pk})


class DealListView(LoginRequiredMixin, DealPermissionMixin, ListView):
    model = Deal
    template_name = "crm/deals/deal_list.html"
    context_object_name = "deals"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_form = DealSearchForm(self.request.GET)

        if search_form.is_valid():
            query = search_form.cleaned_data["q"]
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query)
                    | Q(client__first_name__icontains=query)
                    | Q(client__last_name__icontains=query)
                    | Q(manager__username__icontains=query)
                    | Q(status__icontains=query)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = DealSearchForm(self.request.GET)

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_params"] = query_params.urlencode()

        return context


class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    template_name = "crm/deals/deal_form.html"
    context_object_name = "deal"
    form_class = DealForm
    success_url = reverse_lazy("crm:deal-list")

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)


class DealDetailView(LoginRequiredMixin, DealPermissionMixin, DetailView):
    model = Deal
    template_name = "crm/deals/deal_detail.html"
    context_object_name = "deal"


class DealUpdateView(LoginRequiredMixin, DealPermissionMixin, UpdateView):
    model = Deal
    form_class = DealForm
    template_name = "crm/deals/deal_form.html"
    context_object_name = "deal"
    success_url = reverse_lazy("crm:deal-list")


class DealDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Deal
    template_name = "crm/deals/deal_confirm_delete.html"
    context_object_name = "deal"
    success_url = reverse_lazy("crm:deal-list")
