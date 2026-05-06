from twilio.rest import Client
from src.config.twilio import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER

class WhatsApp:

    @staticmethod
    def send_code(to_number, code):
        if (not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_WHATSAPP_NUMBER or
            TWILIO_ACCOUNT_SID.startswith('your_') or TWILIO_AUTH_TOKEN.startswith('your_') or
            TWILIO_WHATSAPP_NUMBER.startswith('your_')):
            print(f"Twilio credentials not configured. Skipping WhatsApp message to {to_number}. Code: {code}")
            return None

        from_number = TWILIO_WHATSAPP_NUMBER
        if not from_number.startswith('whatsapp:'):
            from_number = f'whatsapp:{from_number}'

        to_number_formatted = to_number
        if not str(to_number_formatted).startswith('whatsapp:'):
            to_number_formatted = f'whatsapp:{to_number_formatted}'

        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Seu código de verificação é: {code}",
                from_=from_number,
                to=to_number_formatted
            )
            return message.sid
        except Exception as e:
            print(f"Twilio send_code error: {e}")
            return None