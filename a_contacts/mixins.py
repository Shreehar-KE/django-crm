from django.contrib import messages


class MessageMixin:
    
    def form_valid(self, form):
        response = super().form_valid(form)

        success_message = getattr(self, "success_message", "Operation successful!")
        messages.success(self.request, success_message)

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        error_message = getattr(
            self, "error_message", "There was an error with your submission."
        )
        messages.error(self.request, error_message)

        return response
