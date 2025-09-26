import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from .models import ClientOnboarding

@receiver(post_save, sender=Ticket)
def notify_ticket_completed(sender, instance, created, **kwargs):
    if instance.status == "Completed":
        phone_number = instance.requester_phone
        access_token = "1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS"
        
        headers_custom_fields = {
            "accept": "application/json",
            "X-ACCESS-TOKEN": access_token,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Define your custom field IDs
        custom_field_level_id = "440961"
        custom_field_status_id = "891576"
        custom_field_ticketid_id = "386473"

        # Fill Ticket Level
        url_level = f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_level_id}"
        data_level = {"value": str(instance.priority)}# Use 'priority' here
        requests.post(url_level, headers=headers_custom_fields, data=data_level)

        # Fill Ticket Status
        url_status = f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_status_id}"
        data_status = {"value": instance.status}
        requests.post(url_status, headers=headers_custom_fields, data=data_status)

        # Fill Ticket ID
        url_ticketid = f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_ticketid_id}"
        data_ticketid = {"value": str(instance.id)}
        requests.post(url_ticketid, headers=headers_custom_fields, data=data_ticketid)

        # Now trigger WhatsApp message API after filling fields
        whatsapp_api_url = f"https://app.speedbots.io/api/contacts/{phone_number}/send/1757347719597"
        headers_whatsapp = {
            "accept": "application/json",
            "X-ACCESS-TOKEN": access_token,
        }
        try:
            response = requests.post(whatsapp_api_url, headers=headers_whatsapp)
            print(f"Notification sent to {phone_number}: {response.status_code}, Response: {response.text}")

        except Exception as e:
            print(f"API notification error: {e}")



@receiver(post_save, sender=Ticket)
def notify_assigned_person_after_ticket_create(sender, instance, created, **kwargs):
    if created:
        phone_number = str(instance.assigned_phone)  
        access_token = "1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS"
        
        headers = {
            "accept": "application/json",
            "X-ACCESS-TOKEN": access_token,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        # Map priority to assign days
        priority_days_map = {
            "High": "2",
            "Medium": "4",
            "Low": "7",
        }
        assign_days_value = priority_days_map.get(instance.priority, "7")
        
        # Use the same API custom fields IDs you already have:
        custom_field_ticketid_id = "890534"
        custom_field_taskname_id = "990016"
        custom_field_taskpriority_id = "381277"
        custom_field_assigndays_id = "510615"
    try:
        # Update custom fields for the contact (assigned person)
        requests.post(
            f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_ticketid_id}",
            headers=headers,
            data={"value": str(instance.id)}
        )
        requests.post(
            f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_taskname_id}",
            headers=headers,
            data={"value": instance.subject}
        )
        requests.post(
            f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_taskpriority_id}",
            headers=headers,
            data={"value": instance.priority}
        )   
        requests.post(
            f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_assigndays_id}",
            headers=headers,
            data={"value": assign_days_value}  # Adjust assign days as needed
        )

        # Trigger WhatsApp flow to send message
        whatsapp_api_url = f"https://app.speedbots.io/api/contacts/{phone_number}/send/1758248114143"
        whatsapp_headers = {
            "accept": "application/json",
            "X-ACCESS-TOKEN": access_token,
        }
        
        response = requests.post(whatsapp_api_url, headers=whatsapp_headers)
        print(f"Sent WhatsApp notification: {response.status_code}, {response.text}")
    except Exception as e:
            print(f"Error sending WhatsApp notification: {e}")


@receiver(post_save, sender=ClientOnboarding)
def notify_assigned_user_new_client(sender, instance, created, **kwargs):
    if created:
        phone_number = str(instance.assigned_phone)
        access_token = "1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS"
        
        headers = {
            "accept": "application/json",
            "X-ACCESS-TOKEN": access_token,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Define your custom field IDs and WhatsApp template ID here
        custom_field_ticketid_id = "YOUR_CUSTOM_FIELD_TICKET_ID"
        whatsapp_template_id = "YOUR_WHATSAPP_TEMPLATE_ID"

        try:
            # Update custom field with client id
            requests.post(
                f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_ticketid_id}",
                headers=headers,
                data={"value": str(instance.id)},
            )

            # Trigger WhatsApp notification
            whatsapp_api_url = f"https://app.speedbots.io/api/contacts/{phone_number}/send/{whatsapp_template_id}"
            response = requests.post(
                whatsapp_api_url,
                headers={
                    "accept": "application/json",
                    "X-ACCESS-TOKEN": access_token,
                }
            )
            print(f"Sent onboarding notification to {phone_number}: Status {response.status_code}")
        except Exception as e:
            print(f"Error sending onboarding notification: {e}")
