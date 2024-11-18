import random
import time
import urllib
from django.http import HttpRequest, HttpResponse
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
    selected_filters = []
    is_result = True
    is_search_text = False
    context_object_name = "contacts"
    template_name = 'a_contacts/home.html'
    paginate_by = 5
    sort_by = None
    order = None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.sort_by = request.GET.get("sort-radio")
        self.order = request.GET.get("order-radio")
        self.selected_filters = request.GET.getlist('type')
        self.search_text = request.GET.get("search_text", "")
        if self.search_text:
            self.search_text = urllib.parse.unquote(self.search_text)
            self.search_text = self.search_text.strip()
            self.is_search_text = True
        return super().get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)

        if self.request.headers.get('Hx-Request'):
            return self.response_class(
                request=self.request,
                template="partials/table_row.html",
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
        search_text_length = len(self.search_text)

        if self.selected_filters:
            contacts = Contact.objects.filter(type__in=self.selected_filters)
            
        else:
            contacts = super().get_queryset()

        if self.sort_by:
            if self.order == 'asc':
                contacts = contacts.order_by(self.sort_by)
            else:
                contacts = contacts.order_by(f'-{self.sort_by}')


        if self.search_text and search_text_length > 3:
            if self.search_text.startswith('#'):
                q = self.search_text[1:].lstrip('0')

                if q.isdigit():
                    id_length = len(q)
                else:
                    self.is_result = False
                    return Contact.objects.none()
                if (id_length in (1, 2) and search_text_length == 4) or (id_length >= 3 and search_text_length == id_length+1):
                    queryset = contacts.filter(contact_id=q)
                else:
                    self.is_result = False
                    return Contact.objects.none()

            else:
                parts = self.search_text.split()

                q = Q(first_name__icontains=parts[0]) | Q(last_name__icontains=parts[0]) | Q(
                    email__icontains=parts[0]) | Q(location__icontains=parts[0]) | Q(type__icontains=parts[0])
                for part in parts[1:]:
                    q |= Q(first_name__icontains=part) | Q(last_name__icontains=part) | Q(
                        email__icontains=part) | Q(location__icontains=part) | Q(type__icontains=part)
                queryset = contacts.filter(q)

            if queryset:
                return queryset
            else:
                self.is_result = False
                return Contact.objects.none()
        else:
            return contacts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_result'] = self.is_result
        context['is_search_text'] = self.is_search_text
        
        if self.is_result and context.get('page_obj'):
            page_obj = context['page_obj']
            context['page_offset'] = (page_obj.number - 1) * self.paginate_by
            context['more_contacts'] = page_obj.has_next()
            context['next_page'] = page_obj.next_page_number() if page_obj.has_next() else None
        else:
            context['page_offset'] = 0
            context['more_contacts'] = False
            context['next_page'] = None
            context['contacts'] = []

        context['lead_count'] = Contact.objects.filter(type='LEAD').count()
        context['prospect_count'] = Contact.objects.filter(
            type='PROSPECT').count()
        context['customer_count'] = Contact.objects.filter(
            type='CUSTOMER').count()
        context['search_text'] = self.search_text
        context['selected_filters'] = self.selected_filters

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
