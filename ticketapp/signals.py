import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from .models import ClientOnboarding
from .models import PaymentPendingClient
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import PaymentPendingClient
from ticketapp.whatsapp_utils import send_whatsapp_alert
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY  # Add your secret key in settings.py  

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
        phone_number = instance.assigned_phone
        if isinstance(phone_number, tuple):
            phone_number = phone_number[0]
        phone_number = str(phone_number)
        access_token = "1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS"
        
        headers = {
            "accept": "application/json",
            "X-ACCESS-TOKEN": access_token,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Define your custom field IDs 
        custom_field_ticketid_id = "824484"
        

        try:
            # Update custom field with client id
            response_cf = requests.post(
                f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_ticketid_id}",                
                headers=headers,
                data={"value": str(instance.id)},
            )
            print(f"Custom field update response: {response_cf.status_code}, {response_cf.text}")
            
            # Trigger WhatsApp notification
            whatsapp_api_url = f"https://app.speedbots.io/api/contacts/{phone_number}/send/1759978132098"
            response = requests.post(
                whatsapp_api_url,
                headers={
                    "accept": "application/json",
                    "X-ACCESS-TOKEN": access_token,
                }
            )
            print(f"WhatsApp send response: {response.status_code}, {response.text}")
            print(f"Sent onboarding notification to {phone_number}: Status {response.status_code}")
        except Exception as e:
            print(f"Error sending onboarding notification: {e}")

# @receiver(post_save, sender=PaymentPendingClient)
# def notify_payment_pending_client(sender, instance, created, **kwargs):
#     if created:
#         phone_number = str(instance.assigned_phone)  # field from your model
#         access_token = "1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS"
        
#         headers = {
#             "accept": "application/json",
#             "X-ACCESS-TOKEN": access_token,
#             "Content-Type": "application/x-www-form-urlencoded",
#         }

#         # Custom field and template IDs (replace with real ones later)
#         custom_field_ticketid_id = "YOUR_CUSTOM_FIELD_TICKET_ID"
#         whatsapp_template_id = "YOUR_WHATSAPP_TEMPLATE_ID"

#         try:
#             # Update custom field with client id
#             requests.post(
#                 f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_ticketid_id}",
#                 headers=headers,
#                 data={"value": str(instance.id)},
#             )

#             # Trigger WhatsApp notification
#             whatsapp_api_url = f"https://app.speedbots.io/api/contacts/{phone_number}/send/{whatsapp_template_id}"
#             response = requests.post(
#                 whatsapp_api_url,
#                 headers={
#                     "accept": "application/json",
#                     "X-ACCESS-TOKEN": access_token,
#                 }
#             )
#             print(f"Sent pending payment notification to {phone_number}: Status {response.status_code}")
#         except Exception as e:
#             print(f"Error sending payment notification: {e}")
            

# @receiver(post_save, sender=PaymentPendingClient)
# def notify_overdue_payment(sender, instance, created, **kwargs):
#     if created:
#         return
#     today = date.today()
#     try:
#         old_instance = PaymentPendingClient.objects.get(pk=instance.pk)
#     except PaymentPendingClient.DoesNotExist:
#         old_instance = None

#     already_overdue_before = (
#         old_instance and old_instance.due_date and today > old_instance.due_date and not old_instance.alert_sent
#     )
#     is_now_overdue = instance.due_date and today > instance.due_date and not instance.alert_sent

#     if is_now_overdue and not already_overdue_before:
#         access_token = "1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS"
#         template_id = "TEST"
#         custom_field_id = "TEST"
#         #  Use instance.client_phone instead
#         success = send_whatsapp_alert(
#             instance.client_phone, instance.id, access_token, template_id, custom_field_id
#         )
#         if success:
#             instance.alert_sent = True
#             instance.save(update_fields=['alert_sent'])
# @receiver(post_save, sender=PaymentPendingClient)
# def notify_overdue_payment(sender, instance, created, **kwargs):
#     if created:
#         return

#     today = date.today()

#     # Check overdue conditions
#     is_now_overdue = instance.due_date and today > instance.due_date and not instance.alert_sent
#     if is_now_overdue:
#         print(f"Client {instance.client_name} is now overdue. Generating Stripe link...")

#         # Generate a Stripe payment link for the overdue amount
#         desc = f"Overdue payment for {instance.client_name}"
#         payment_url = create_stripe_payment_link(instance.payment_amount, desc)

#         if payment_url:
#             print(f"Stripe payment link created: {payment_url}")

#             # Send WhatsApp message with payment link
#             access_token = "1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS"
#             message_text = (
#                 f"Dear {instance.client_name}, your payment of ₹{instance.payment_amount} is overdue.\n"
#                 f"Please pay securely via Stripe: {payment_url}"
#             )

#             # You can adapt this to call WhatsApp API as a message
#             success = send_whatsapp_alert(
#                 instance.client_phone, instance.id, access_token, "TEST", "TEST"
#             )
#             if success:
#                 instance.alert_sent = True
#                 instance.save(update_fields=['alert_sent'])
#                 print("Payment link sent successfully.")
#             else:
#                 print("Failed to send notification.")
# @receiver(post_save, sender=PaymentPendingClient)
# def notify_overdue_payment(sender, instance, created, **kwargs):
#     if created:
#         return

#     today = date.today()

#     is_now_overdue = instance.due_date and today > instance.due_date and not instance.alert_sent
#     print("notify_overdue_payment signal received")

#     if is_now_overdue:
#         print(f"Client {instance.client_name} is now overdue. Generating Stripe link...")

#         # Generate a Stripe payment link for the overdue amount
#         desc = f"Overdue payment for {instance.client_name}"
#         print("Reached overdue block, about to generate payment link.")
#         payment_url = create_stripe_payment_link(instance.payment_amount, desc)
#         print("Payment URL after calling create_stripe_payment_link():", payment_url)
#         if payment_url:
#             message_text = (
#                 f"Dear {instance.client_name}, your payment of ₹{instance.payment_amount} is overdue.\n"
#                 f"Please pay securely via Stripe: {payment_url}"
#             )

#             # Debug prints for message content and payment URL
#             print("Prepared WhatsApp message to send:")
#             print(message_text)
#             print(f"Payment URL: {payment_url}")

#             # Call the WhatsApp alert function (adapt if it supports message_text)
#             success = send_whatsapp_alert(
#                 instance.client_phone, instance.id, access_token="1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS",
#                 template_id="TEST", custom_field_id="TEST"
#             )
#             if success:
#                 instance.alert_sent = True
#                 instance.save(update_fields=['alert_sent'])
#                 print("Payment link sent successfully.")
#             else:
#                 print("Failed to send notification.")

            
# def create_stripe_payment_link(amount, description):
#     print(f"[Mock] Stripe link created for amount: {amount}, desc: {description}")
#     return "https://stripe.com/mock-payment-link"

            
# def create_stripe_payment_link(amount, description):
#     payment_link = stripe.PaymentLink.create(
#         line_items=[{
#             'price_data': {
#                 'currency': 'inr',
#                 'unit_amount': int(amount * 100),  # If amount in rupees
#                 'product_data': {
#                     'name': description,
#                 },
#             },
#             'quantity': 1,
#         }],
#         after_completion={
#             'type': 'redirect',
#             'redirect': {'url': 'https://yourdomain.com/payment-success/'}
#         }
#     )
#     return payment_link.url     

        #   working one 
# from datetime import date
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import PaymentPendingClient
# from ticketapp.whatsapp_utils import send_whatsapp_alert
# from datetime import datetime, date

# def to_date(val):
#     if isinstance(val, date):
#         return val
#     if isinstance(val, str):
#         try:
#             return datetime.strptime(val, "%Y-%m-%d").date()
#         except:
#             return None
#     return None

# @receiver(post_save, sender=PaymentPendingClient)
# def notify_overdue_payment(sender, instance, created, **kwargs):
#     print("notify_overdue_payment signal received")
#     if created:
#         print(f"New client created: {instance.client_name}, due date: {instance.due_date}")
#         return

#     today = date.today()

#     is_now_overdue = instance.due_date and today > instance.due_date and not instance.alert_sent
#     print("notify_overdue_payment signal received")

#     if is_now_overdue:
#         print(f"Client {instance.client_name} is now overdue. Generating Stripe link...")

#         desc = f"Overdue payment for {instance.client_name}"
#         print("Reached overdue block, about to generate payment link.")
#         payment_url = create_stripe_payment_link(instance.payment_amount, desc)
#         print("Payment URL after calling create_stripe_payment_link():", payment_url)

#         if payment_url:
#             message_text = (
#                 f"Dear {instance.client_name}, your payment of ₹{instance.payment_amount} is overdue.\n"
#                 f"Please pay securely via Stripe: {payment_url}"
#             )

#             # Debug prints for message content and payment URL
#             print("Prepared WhatsApp message to send:")
#             print(message_text)
#             print(f"Payment URL: {payment_url}")

#             # Call WhatsApp alert function
#             success = send_whatsapp_alert(
#                 instance.client_phone, instance.id,
#                 access_token="1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS",
#                 template_id="TEST",
#                 custom_field_id="TEST"
#             )
#             if success:
#                 instance.alert_sent = True
#                 instance.save(update_fields=['alert_sent'])
#                 print("Payment link sent successfully.")
#             else:
#                 print("Failed to send notification.")

# def create_stripe_payment_link(amount, description):
#     print(f"[Mock] Stripe link created for amount: {amount}, desc: {description}")
#     return "https://stripe.com/mock-payment-link"


# from datetime import date
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import PaymentPendingClient
# from ticketapp.whatsapp_utils import send_whatsapp_alert
# from datetime import datetime, date

# def to_date(value):
#     if isinstance(value, date):
#         return value
#     if isinstance(value, str):
#         try:
#             return datetime.strptime(value, "%Y-%m-%d").date()
#         except ValueError:
#             return None
#     return None
# @receiver(post_save, sender=PaymentPendingClient)
# def notify_overdue_payment(sender, instance, created, **kwargs):
#     print("notify_overdue_payment signal received")
    
#     due_date = to_date(instance.due_date)
#     today = date.today()

#     # Run on create OR if overdue on update
#     if created or (due_date and date.today() > due_date and not instance.alert_sent):
#         print(f"Processing payment notification for client {instance.client_name}")

#         desc = f"Overdue payment for {instance.client_name}"
#         payment_url = create_stripe_payment_link(instance.payment_amount, desc)
#         print("Payment URL after calling create_stripe_payment_link():", payment_url)

#         if payment_url:
#             message_text = (
#                 f"Dear {instance.client_name}, your payment of ₹{instance.payment_amount} is overdue.\n"
#                 f"Please pay securely via Stripe: {payment_url}"
#             )
#             print("Prepared WhatsApp message to send:")
#             print(message_text)

#             # Call WhatsApp alert function
#             success = send_whatsapp_alert(
#                 instance.client_phone, instance.id,
#                 access_token="1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS",
#                 template_id="1757347719597",
#                 custom_field_id="824484"
#             )
#             if success:
#                 instance.alert_sent = True
#                 instance.save(update_fields=['alert_sent'])
#                 print("Payment link sent successfully.")
#             else:
#                 print("Failed to send notification.")
#     else:
#         print("No payment notification sent (not overdue or already alerted)")

# def create_stripe_payment_link(amount, description):
#     print(f"[Mock] Stripe link created for amount: {amount}, desc: {description}")
#     return "https://stripe.com/mock-payment-link"
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PaymentPendingClient
from ticketapp.whatsapp_utils import send_whatsapp_alert
from datetime import datetime, date

def to_date(value):
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None
@receiver(post_save, sender=PaymentPendingClient)
def notify_overdue_payment(sender, instance, created, **kwargs):
    print("notify_overdue_payment signal received")

    due_date = to_date(instance.due_date)
    today = date.today()

    if created or (due_date and today > due_date and not instance.alert_sent):
        print(f"Processing payment notification for client {instance.client_name}")

        desc = f"Overdue payment for {instance.client_name}"

        try:
            amount = float(instance.payment_amount)
            print("Sanitized payment amount as float:", amount)
        except Exception as e:
            print(f"Invalid payment amount: {instance.payment_amount}, error: {e}")
            return  # Exit early since amount invalid

        payment_url = create_stripe_payment_link(amount, desc)
        print("Payment URL after calling create_stripe_payment_link():", payment_url)

        if payment_url:
            message_text = (
                f"Dear {instance.client_name}, your payment of ₹{amount} is overdue.\n"
                f"Please pay securely via Stripe: {payment_url}"
            )
            print("Prepared WhatsApp message to send:")
            print(message_text)

            # Call WhatsApp alert function
            success = send_whatsapp_alert(
                instance.client_phone, instance.id,
                payment_url = payment_url,
                access_token="1454240.ma5kfaevUoUzpTQQD5JBianwx22KFLwpClDdqGEQTS",
                template_id="1760521228933",
                custom_field_id="668381",
                message_text=message_text
            )
            if success:
                instance.alert_sent = True
                instance.save(update_fields=['alert_sent'])
                print("Payment link sent successfully.")
            else:
                print("Failed to send notification.")
    else:
        print("No payment notification sent (not overdue or already alerted)")

def create_stripe_payment_link(amount, description):
    print("Amount to be charged (in paise):", int(amount * 100))
    payment_link = stripe.PaymentLink.create(
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(amount * 100),  # If amount in rupees
                'product_data': {
                    'name': description,
                },
            },
            'quantity': 1,
        }],
        after_completion={
            'type': 'redirect',
            'redirect': {'url': 'https://yourdomain.com/payment-success/'}
        }
    )
    return payment_link.url