from django.apps import AppConfig


class TicketappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticketapp'

    def ready(self):
            import ticketapp.signals  # This ensures signals are registered when the app loads
