from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, UpdateView
from django.core.exceptions import PermissionDenied

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
    model = get_user_model()
    template_name = "employee/employee_list.html"
    context_object_name = "employees"


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "employee/employee_detail.html"
    context_object_name = "employee"


class EmployeeUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = EmployeeUpdateForm
    template_name = "employee/employee_update.html"
    context_object_name = "employee"

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@login_required
def employeeDeleteView(request, pk):
    if request.user.pk == pk:
        user = get_object_or_404(get_user_model(), id=pk)

        if request.method == "POST":
            user.delete()
            return redirect("a_contacts:home")
        else:
            context = {"user": user}
            return render(request, "partials/user_delete_confirm.html", context)
    else:
        raise PermissionDenied()
