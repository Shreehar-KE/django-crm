from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, UpdateView

from .models import CustomUser


def approval_status(request):
    if request.user.is_authenticated and not request.user.is_approved:
        return render(
            request,
            "account/approval_status.html",
            {"approval_status": request.user.approval_status},
        )
    else:
        return redirect("a_contacts:home")


class EmployeeListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "employee/employee_list.html"
    context_object_name = "employees"


class EmployeeDetailView(DetailView):
    model = CustomUser
    template_name = "employee/employee_detail.html"
    context_object_name = "employee"


class EmployeeUpdateView(UpdateView):
    pass


def employeeDeleteView(request):
    pass
