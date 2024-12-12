import random
import csv
import urllib
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView)
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Contact
from .forms import ContactForm, ContactBulkCreateForm
from faker import Faker
from .templatetags.templatetags import format_contact_id
from analytics.models import Like


class HomePageView(ListView):
    model = Contact
    search_text = ''
    selected_filters = []
    is_result = True
    is_search_text = False
    context_object_name = "contacts"
    template_name = 'a_contacts/home.html'
    paginate_by = 20
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
            if page_obj.has_next():
                context['next_page'] = page_obj.next_page_number()
            else:
                context['next_page'] = None
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
        context['likes'] = Like.objects.count()

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

    return render(request, 'partials/contact_form.html', {'form': form})


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    context_object_name = 'contact'
    template_name = 'a_contacts/contact_update.html'


class ContactDetailView(DetailView):
    model = Contact
    context_object_name = "contact"
    template_name = 'a_contacts/contact_detail.html'


def contactBulkCreateView(request):
    if request.method == 'GET' and request.headers.get('Hx-Request'):
        form = ContactBulkCreateForm()
        return render(request, 'partials/contact_bulk_create_modal_form.html', {'form': form})
    elif request.method == 'POST' and request.FILES.get('csv_file'):
        form = ContactBulkCreateForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            valid_data = []
            invalid_data = []

            for row in csv_reader:
                try:
                    obj = Contact(**row)
                    obj.full_clean()
                    valid_data.append(row)
                except ValidationError as e:
                    row['errors'] = e.message_dict
                    invalid_data.append(row)

            request.session['preview_data'] = valid_data
            request.session['invalid_data'] = invalid_data

            return JsonResponse({'redirect': '/contact/bulkcreate/preview/'})
        else:
            return render(request, 'partials/contact_bulk_create_modal_form.html', {'form': form})
    else:
        return redirect('a_contacts:home')


def contactBulkCreatePreview(request):
    valid_data = request.session.get('preview_data', [])
    invalid_data = request.session.get('invalid_data', [])

    if request.method == 'POST':
        for row in valid_data:
            Contact.objects.create(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                location=row['location'],
                type=row['type']
            )

        request.session.pop('preview_data', None)
        request.session.pop('invalid_data', None)

        return redirect('a_contacts:home')

    formatted_valid_data = [list(row.values()) for row in valid_data]
    formatted_invalid_data = [list(row.values()) for row in invalid_data]

    return render(request, 'a_contacts/bulk_create_preview.html', {
        'valid_data': formatted_valid_data,
        'invalid_data': formatted_invalid_data,
    })


def exportRandomDataCSV(request):
    if 'HTTP_REFERER' in request.META and 'contact/create' in request.META['HTTP_REFERER']:
        faker = Faker()
        headers = ['first_name', 'last_name', 'email', 'location', 'type']
        data = []
        for _ in range(10):
            fake_name = faker.name()
            first_name = fake_name.split()[0]
            last_name = fake_name.split()[1]
            types = [Contact.Type.LEAD,
                     Contact.Type.PROSPECT, Contact.Type.CUSTOMER]

            data.append({
                "first_name": first_name,
                "last_name": last_name,
                "email": f'{first_name.lower()}.{last_name.lower()}@email.com',
                "location": faker.country(),
                "type": random.choice(types)
            })

        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="random_data.csv"'},
        )

        writer = csv.DictWriter(response, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

        return response
    else:
        return redirect('a_contacts:home')


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


def exportDataCSV(request):
    data = []

    contacts = Contact.objects.all()
    if contacts:
        for contact in contacts:
            data.append({
                "id": format_contact_id(contact.contact_id),
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "email": contact.email,
                "location": contact.location,
                "type": contact.type,
            })
        messages.success(request, "CSV data exported successfully.")
    else:
        messages.error(request, "CSV data failed to export.")
    response = JsonResponse(data, safe=False, status=204)
    return response


def exportDataPDF(request):
    data = []

    contacts = Contact.objects.all()
    if contacts:
        for contact in contacts:
            data.append({
                "id": format_contact_id(contact.contact_id),
                "name": contact.first_name +" "+ contact.last_name,
                "email": contact.email,
                "location": contact.location,
                "type": contact.type,
            })
        messages.success(request, "PDF data exported successfully.")
    else:
        messages.error(request, "PDF data failed to export.")
    response = JsonResponse(data, safe=False, status=204)
    return response
