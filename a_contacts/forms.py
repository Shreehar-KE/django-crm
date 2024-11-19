from django.forms import ModelForm, TextInput, Select, ClearableFileInput
from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            'first_name': TextInput(attrs={
                'id': 'first-name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5',
            }),
            'last_name': TextInput(attrs={
                'id': 'last-name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5',
            }),
            'email': TextInput(attrs={
                'id': 'email',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5',
            }),
            'location': TextInput(attrs={
                'id': 'location',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5',
            }),
            'type': Select(attrs={
                'id': 'type',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5',
            }),
            'image': ClearableFileInput(attrs={
                'id': 'image-input',
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 p-1.5 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
            }),
        }
