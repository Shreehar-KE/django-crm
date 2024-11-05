from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, TemplateView, CreateView, UpdateView, DetailView)
from .models import Contact
from .forms import ContactForm


class HomePageView(ListView):
    model = Contact
    context_object_name = "contacts"
    ordering = "first_name"
    template_name = 'a_contacts/home.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['lead_count'] = Contact.objects.filter(type='LEAD').count()
        context['prospect_count'] = Contact.objects.filter(type='PROSPECT').count()
        context['customer_count'] = Contact.objects.filter(type='CUSTOMER').count()

        return context

class ContactCreateView(CreateView):
    form_class = ContactForm
    template_name = 'a_contacts/contact_create.html'


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'a_contacts/contact_update.html'


class ContactDetailView(DetailView):
    model = Contact
    context_object_name = "contact"
    template_name = 'a_contacts/contact_detail.html'


def contactDeleteView(request, pk):
    contact = get_object_or_404(Contact, id=pk)

    if (request.method == 'POST'):
        contact.delete()
        return redirect('a_contacts:home')

    return render(request, 'partials/contact_delete_confirm.html', {'contact': contact})
