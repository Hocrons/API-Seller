# from twilio.rest import Client
# from src.config.twilio import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER

# class WhatsApp:

#     @staticmethod
#     def send_code(to_number, code):
#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#         message = client.messages.create(
#             body=f"Seu código de verificação é: {code}",
#             from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
#             to=f"whatsapp:{to_number}"
#         )

#         return message.sid

from twilio.rest import Client
from src.config.twilio import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER

class WhatsApp:

    @staticmethod
    def send_code(to_number, code):
        print("SID:", TWILIO_ACCOUNT_SID)
        print("TOKEN EXISTS:", TWILIO_AUTH_TOKEN is not None)
        print("FROM:", TWILIO_WHATSAPP_NUMBER)
        print("TO:", to_number)

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Seu código de verificação é: {code}",
            from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
            to=f"whatsapp:{to_number}"
        )

        return message.sid