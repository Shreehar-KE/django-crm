from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, TemplateView, CreateView, UpdateView, DetailView)
from .models import Contact
from .forms import ContactForm


class HomePageView(ListView):
    model = Contact
    context_object_name = "contacts"
    ordering = "first_name"
    template_name = 'a_contacts/main.html'


class ContactCreateView(CreateView):
    form_class = ContactForm
    template_name = 'a_contacts/contact_create.html'
    success_url = reverse_lazy("a_contacts:home")


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'a_contacts/contact_update.html'
    success_url = reverse_lazy("a_contacts:home")


class ContactDetailView(DetailView):
    model = Contact
    context_object_name = "contact"
    template_name = 'a_contacts/contact_detail.html'
