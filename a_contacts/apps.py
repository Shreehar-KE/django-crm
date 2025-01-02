from django.apps import AppConfig


class ACustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "a_contacts"

    def ready(self):
        import a_contacts.signals

        return super().ready()
