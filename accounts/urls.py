from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("employee/approval-status/", views.approval_status, name="approval_status"),
    path("employees/", views.EmployeeListView.as_view(), name="employee-list"),
    path(
        "employee/<uuid:pk>/",
        views.EmployeeDetailView.as_view(),
        name="employee-detail",
    ),
    path(
        "employee/<uuid:pk>/update/",
        views.EmployeeUpdateView.as_view(),
        name="employee-update",
    ),
    path(
        "employee/<uuid:pk>/delete/",
        views.employeeDeleteView,
        name="employee-delete",
    ),
]
