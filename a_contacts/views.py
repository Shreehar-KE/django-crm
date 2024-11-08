import random
import urllib
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView)
from django.db.models import Q
from .models import Contact
from .forms import ContactForm
from faker import Faker


class HomePageView(ListView):
    model = Contact
    search_text = ''
    context_object_name = "contacts"
    ordering = "first_name"
    template_name = 'a_contacts/home.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)

        if self.request.headers.get('Hx-Request'):

            return self.response_class(
                request=self.request,
                template="includes/table_data.html",
                context=context,
                using=self.template_engine,
                **response_kwargs,
            )
        else:
            return self.response_class(
                request=self.request,
                template=self.get_template_names(),
                context=context,
                using=self.template_engine,
                **response_kwargs,
            )

    def get_queryset(self):
        self.search_text = self.request.GET.get("search_text", "")
        self.search_text = urllib.parse.unquote(self.search_text)
        self.search_text = self.search_text.strip()

        if self.search_text and len(self.search_text) > 3:
            if self.search_text.startswith('#'):
                q = self.search_text[1:].lstrip('0')
                return Contact.objects.filter(contact_id=q)

            parts = self.search_text.split()

            q = Q(first_name__icontains=parts[0]) | Q(last_name__icontains=parts[0]) | Q(
                email__icontains=parts[0]) | Q(location__icontains=parts[0]) | Q(type__icontains=parts[0])
            for part in parts[1:]:
                q |= Q(first_name__icontains=part) | Q(last_name__icontains=part) | Q(
                    email__icontains=part) | Q(location__icontains=part) | Q(type__icontains=part)
            return Contact.objects.filter(q)
        else:
            return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lead_count'] = Contact.objects.filter(type='LEAD').count()
        context['prospect_count'] = Contact.objects.filter(
            type='PROSPECT').count()
        context['customer_count'] = Contact.objects.filter(
            type='CUSTOMER').count()
        context['search_text'] = self.search_text

        return context


class ContactCreateView(CreateView):
    form_class = ContactForm
    template_name = 'a_contacts/contact_create.html'


def fillContactForm(request):
    faker = Faker()
    fake_name = faker.name()

    first_name = fake_name.split()[0]
    last_name = fake_name.split()[1]
    types = [Contact.Type.LEAD, Contact.Type.PROSPECT, Contact.Type.CUSTOMER]

    fake_contact = {
        "first_name": first_name,
        "last_name": last_name,
        "email": f'{first_name.lower()}.{last_name.lower()}@email.com',
        "location": faker.country(),
        "type": random.choice(types)
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
