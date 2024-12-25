from django.views.generic import TemplateView
from django.shortcuts import render, redirect

def approval_status(request):
    if request.user.is_authenticated and not request.user.is_approved:
        return render(
            request,
            "account/approval_status.html",
            {"approval_status": request.user.approval_status},
        )
    else:
        return redirect("a_contacts:home")

class EmployeeDetailView(TemplateView):
    template_name = "404.html"