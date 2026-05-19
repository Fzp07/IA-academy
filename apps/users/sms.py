from django.conf import settings

def send_sms(to_number, message):
    try:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_number = settings.TWILIO_FROM_NUMBER
        if not all([account_sid, auth_token, from_number]):
            print(f'[SMS] A: {to_number} - Mensaje: {message}')
            return True
        from twilio.rest import Client
        client = Client(account_sid, auth_token)
        client.messages.create(body=message, from_=from_number, to=to_number)
        return True
    except Exception as e:
        print(f'[SMS Error] {e}')
        print(f'[SMS] A: {to_number} - Mensaje: {message}')
        return False
