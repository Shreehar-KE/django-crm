from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from .models import Contact
from .forms import ContactForm


class HomePageView(ListView):
    model = Contact
    context_object_name = "contacts"
    ordering = "first_name"
    template_name = 'a_contacts/table.html'


class ContactCreateView(CreateView):
    form_class = ContactForm
    template_name = 'a_contacts/contact_create.html'
    success_url = reverse_lazy("a_contacts:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = "Create Contact"
        context['button_text'] = "Add Contact"
        return context


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'a_contacts/contact_create.html'
    success_url = reverse_lazy("a_contacts:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = "Update Contact"
        context['button_text'] = "Update Contact"
        return context
