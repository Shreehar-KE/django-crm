from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, UpdateView

from .models import CustomUser
from .forms import EmployeeUpdateForm


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
    model = CustomUser
    form_class = EmployeeUpdateForm
    template_name = "employee/employee_update.html"
    context_object_name = "employee"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def employeeDeleteView(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    origin_url = request.META["HTTP_REFERER"]

    if request.method == "POST":
        user.delete()
        return redirect("a_contacts:home")
    else:
        context = {"user": user}
        return render(request, "partials/user_delete_confirm.html", context)
