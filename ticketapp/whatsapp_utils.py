# import requests

# def send_whatsapp_alert(phone_number, client_id, access_token, template_id, custom_field_id):
#     headers = {
#         "accept": "application/json",
#         "X-ACCESS-TOKEN": access_token,
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     try:
#         # Update custom field (e.g., client id)
#         requests.post(
#             f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_id}",
#             headers=headers,
#             data={"value": str(client_id)},
#         )
#         # Send WhatsApp template message
#         response = requests.post(
#             f"https://app.speedbots.io/api/contacts/{phone_number}/send/{template_id}",
#             headers={"accept": "application/json", "X-ACCESS-TOKEN": access_token}
#         )
#         return response.status_code == 200
#     except Exception as e:
#         print(f"WhatsApp API error: {e}")
#         return False
# import traceback
# print("=== WhatsApp Alert Triggered ===")
# print("Call Stack:")
# traceback.print_stack()

# import requests
# def send_whatsapp_alert(phone_number, client_id, access_token, template_id, custom_field_id,payment_url, message_text=None,):
#     headers = {
#         "accept": "application/json",
#         "X-ACCESS-TOKEN": access_token,
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     try:
#         # Update custom field as usual
#         requests.post(
#             f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_id}",
#             headers=headers,
#             data={"value": payment_url},
#             # data={"value": str(client_id)},
#         )
#         # if message_text:
#         #     # Change URL if your API supports sending raw text
#         #     response = requests.post(
#         #         f"https://app.speedbots.io/api/contacts/{phone_number}/send-text",
#         #         headers={"accept": "application/json", "X-ACCESS-TOKEN": access_token},
#         #         data={"message": message_text}
#             # )
#         # else:
#             # Send WhatsApp template as backup
#         response = requests.post(
#                 f"https://app.speedbots.io/api/contacts/{phone_number}/send/{template_id}",
#                 headers={"accept": "application/json", "X-ACCESS-TOKEN": access_token}
#             )
#         print(f"WhatsApp API response: {response.status_code}, {response.text}")

#         return response.status_code == 200
#     except Exception as e:
#         print(f"WhatsApp API error: {e}")
#         return False
################workingone############
# import requests
# import traceback
# print("=== WhatsApp Alert Triggered ===")
# print("Call Stack:")
# traceback.print_stack()
# def send_whatsapp_alert(phone_number, client_id, access_token, template_id, custom_field_id,payment_url,message_text=None):
#     headers = {
#         "accept": "application/json",
#         "X-ACCESS-TOKEN": access_token,
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     try:
#         print("=== WhatsApp Alert Triggered ===")
#         print(f"Target phone number: {phone_number}")
#         print(f"Client ID: {client_id}")
#         print(f"Template ID: {template_id}")
#         print(f"Custom Field ID: {custom_field_id}")
#         print("Headers:", headers)
        
#         # Update custom field (mock/dry run if IDs dummy)
#         print("Attempting custom field update POST...")
#         response_cf = requests.post(
#             f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_id}",
#             headers=headers,
#             data={"value": payment_url},
#             # data={"value": str(client_id)},
#         )
#         print(f"Custom field update response: {response_cf.status_code}, {response_cf.text}")

#         print("Attempting WhatsApp template POST...")
#         # Send WhatsApp template message
#         response = requests.post(
#             f"https://app.speedbots.io/api/contacts/{phone_number}/send/{template_id}",
#             headers={"accept": "application/json", "X-ACCESS-TOKEN": access_token}
#         )
#         print(f"WhatsApp template send response: {response.status_code}, {response.text}")

#         return response.status_code == 200
#     except Exception as e:
#         print(f"WhatsApp API error: {e}")
#         return False

import requests
import traceback

def send_whatsapp_alert(phone_number, client_id, access_token, template_id, custom_field_id, payment_url, message_text=None):
    headers_json = {
        "accept": "application/json",
        "X-ACCESS-TOKEN": access_token,
        "Content-Type": "application/json",
    }

    headers_form = {
        "accept": "application/json",
        "X-ACCESS-TOKEN": access_token,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        print("=== WhatsApp Alert Triggered ===")
        print(f"Target phone number: {phone_number}")
        print(f"Client ID: {client_id}")
        print(f"Template ID: {template_id}")
        print(f"Custom Field ID: {custom_field_id}")
        print("Headers:", headers_json)

        # Step 1: Create (or ensure) contact
        print("📱 Creating contact...")
        contact_data = {"phone": f"+{phone_number}"}
        response_create = requests.post(
            "https://app.speedbots.io/api/contacts",
            headers=headers_json,
            json=contact_data
        )
        print(f"Contact creation response: {response_create.status_code}, {response_create.text}")

        if response_create.status_code not in [200, 201]:
            print("⚠️ Contact creation failed, aborting further requests.")
            return False

        # Step 2: Update custom field (attach payment info)
        print("🔄 Updating custom field...")
        response_cf = requests.post(
            f"https://app.speedbots.io/api/contacts/{phone_number}/custom_fields/{custom_field_id}",
            headers=headers_form,
            data={"value": payment_url},
        )
        print(f"Custom field update response: {response_cf.status_code}, {response_cf.text}")

        # Step 3: Send message via template
        print("💬 Sending WhatsApp message...")
        response_msg = requests.post(
            f"https://app.speedbots.io/api/contacts/{phone_number}/send/{template_id}",
            headers={"accept": "application/json", "X-ACCESS-TOKEN": access_token},
        )
        print(f"WhatsApp template send response: {response_msg.status_code}, {response_msg.text}")

        return response_msg.status_code == 200

    except Exception as e:
        print(f"❌ WhatsApp API error: {str(e)}")
        traceback.print_exc()
        return False
