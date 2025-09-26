from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from ticketapp.models import ClientOnboarding
import requests

class Command(BaseCommand):
    help = 'Send onboarding deadline reminders to assigned users 1 day before deadline'

    def handle(self, *args, **options):
        # Today + 1 day is target deadline date
        target_date = now().date() + timedelta(days=1)

        # Filter clients where created_at + onboarding_deadline_days == target_date and not onboarded yet
        clients_to_notify = ClientOnboarding.objects.filter(
            created_at__date__lte=target_date,
            onboarding_deadline_days__isnull=False,
            onboarding_completed=False  # Assuming you track completion status
        )

        access_token = "1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS"

        headers = {
            "accept": "application/json",
            "X-ACCESS-TOKEN": access_token,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        custom_field_ticketid_id = "PUT_YOUR_CUSTOM_FIELD_ID_HERE"  # Change as per your API fields

        for client in clients_to_notify:
            phone_number = client.assigned_phone
            try:
                # Optional: update custom fields if needed, example:
                url_custom_field = f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_ticketid_id}"
                requests.post(url_custom_field, headers=headers, data={"value": client.id})

                # Trigger WhatsApp message API (replace YOUR_TEMPLATE_ID)
                whatsapp_api_url = f"https://app.speedbots.io/api/contacts/{phone_number}/send/YOUR_TEMPLATE_ID"
                response = requests.post(whatsapp_api_url, headers=headers)

                self.stdout.write(f"Sent notification to {phone_number}: Status {response.status_code}")
            except Exception as e:
                self.stderr.write(f"Error sending notification to {phone_number}: {str(e)}")
