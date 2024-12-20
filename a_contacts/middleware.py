from django.contrib.messages import get_messages
from django.template.loader import render_to_string


class HtmxMessagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            "Hx-Request" in request.headers
            and get_messages(request)
            and getattr(response, "htmx_toast", True)
        ):
            messages = get_messages(request)
            response.content += render_to_string(
                template_name="includes/toast.html",
                context={"messages": messages},
                request=request,
            ).encode("utf-8")
            response["Content-Type"] = "text/html"

        return response
