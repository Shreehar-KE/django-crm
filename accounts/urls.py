from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("approval-status/", views.approval_status, name="approval_status"),
    path(
        "employee/<uuid:pk>/", views.EmployeeDetailView.as_view(), name="employee-detail"
    ),
]
