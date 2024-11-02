from django.shortcuts import render
from django.views.generic import ListView
from .models import Contact


class HomePageView(ListView):
    model = Contact
    context_object_name = "contacts"
    template_name = 'a_customers/table.html'

