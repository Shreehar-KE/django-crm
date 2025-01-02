from allauth.account.forms import ChangePasswordForm, ResetPasswordKeyForm, SignupForm
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.forms import FileInput, ModelForm, Select, TextInput


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = None
        self.fields["oldpassword"].widget.attrs["placeholder"] = ""
        self.fields["password1"].widget.attrs["placeholder"] = ""
        self.fields["password2"].widget.attrs["placeholder"] = ""


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = None
        self.fields["password1"].widget.attrs["placeholder"] = ""
        self.fields["password2"].widget.attrs["placeholder"] = ""


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = None
        self.fields["email"].unique = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "An account with this username address already exists."
            )
        if username.lower() in settings.ACCOUNT_USERNAME_BLACKLIST:
            raise forms.ValidationError("This username is not allowed.")

        return username


class EmployeeUpdateForm(ModelForm):
    error_css_class = "error"

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "location", "role", "image"]
        widgets = {
            "first_name": TextInput(
                attrs={
                    "id": "first-name",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5",
                }
            ),
            "last_name": TextInput(
                attrs={
                    "id": "last-name",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5",
                }
            ),
            "email": TextInput(
                attrs={
                    "id": "email",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5",
                }
            ),
            "location": TextInput(
                attrs={
                    "id": "location",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5",
                }
            ),
            "role": Select(
                attrs={
                    "id": "type",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:border-primary-500 block w-full p-2.5",
                }
            ),
            "image": FileInput(
                attrs={
                    "id": "image-input",
                    "class": "block w-full text-sm text-gray-900 border border-gray-300 p-1.5 rounded-lg cursor-pointer bg-gray-50 focus:outline-none",
                    "x-ref": "fileInput",
                    "@change": "previewImage($event)",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [("MANAGER", "Manager"), ("AGENT", "Agent")]
