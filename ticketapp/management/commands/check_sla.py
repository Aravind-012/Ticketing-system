from django.core.management.base import BaseCommand
from django.utils.timezone import now
from ticketapp.models import Ticket

class Command(BaseCommand):
    help = 'Check SLA deadlines and escalate overdue tickets'

    def handle(self, *args, **kwargs):
        overdue_tickets = Ticket.objects.filter(
            sla_due_at__lt=now(),
            is_escalated=False,
        ).exclude(status='Completed')

        self.stdout.write(f"Found {overdue_tickets.count()} overdue tickets")

        for ticket in overdue_tickets:
            ticket.is_escalated = True
            ticket.save()
            self.stdout.write(f"Escalated Ticket ID {ticket.id} subject '{ticket.subject}'")
