from django.urls import path

from .views import (
    index,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClientCreateView,
    ClientDeleteView,
)


app_name = "crm"

urlpatterns = [
    path("", index, name="index"),
    path("clients/", ClientListView.as_view(), name="client-list"),
    path("clients/create/", ClientCreateView.as_view(), name="client-create"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client-update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client-delete"),
]
