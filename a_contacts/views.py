import random
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, TemplateView, CreateView, UpdateView, DetailView)
from .models import Contact
from .forms import ContactForm
from faker import Faker


class HomePageView(ListView):
    model = Contact
    context_object_name = "contacts"
    ordering = "first_name"
    template_name = 'a_contacts/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lead_count'] = Contact.objects.filter(type='LEAD').count()
        context['prospect_count'] = Contact.objects.filter(
            type='PROSPECT').count()
        context['customer_count'] = Contact.objects.filter(
            type='CUSTOMER').count()

        return context


class ContactCreateView(CreateView):
    form_class = ContactForm
    template_name = 'a_contacts/contact_create.html'


def fillContactForm(request):
    faker = Faker()
    fake_name = faker.name()
    first_name = fake_name.split()[0]
    last_name = fake_name.split()[1]
    fake_contact = {
        "first_name" : first_name,
        "last_name" : last_name,
        "email" : f'{first_name.lower()}.{last_name.lower()}@email.com',
        "location" : faker.country(),
        "type" : random.choice(['Lead', 'Prospect', 'Customer'])
    }
    form = ContactForm(initial=fake_contact)

    return render(request, 'partials/contact_create_form.html', {'form': form})


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
    origin_url = request.META["HTTP_REFERER"]

    if (request.method == 'POST'):
        contact.delete()
        if "contact" not in origin_url:
            return HttpResponse('', status=200)
        else:
            return redirect('a_contacts:home')

    context = {'contact': contact}

    if "contact" not in origin_url:
        context['homepage'] = True

    return render(request, 'partials/contact_delete_confirm.html', context)
