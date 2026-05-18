from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms.search_form import SearchForm
from .models import Client


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "crm/base.html")


class ClientListView(ListView):
    model = Client
    template_name = "crm/clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data["q"]
            if query:
                queryset = queryset.filter(first_name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


class ClientCreateView(CreateView):
    model = Client
    template_name = "crm/clients/client_form.html"
    context_object_name = "client"
    fields = ["first_name", "last_name", "email", "phone", "company"]
    success_url = reverse_lazy("crm:client-list")

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client
    template_name = "crm/clients/client_detail.html"
    context_object_name = "client"


class ClientUpdateView(UpdateView):
    model = Client
    template_name = "crm/clients/client_form.html"
    context_object_name = "client"
    fields = ["first_name", "last_name", "email", "phone", "company"]
    success_url = reverse_lazy("crm:client-list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "crm/clients/client_confirm_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("crm:client-list")
