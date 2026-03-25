from twilio.rest import Client
import os
import random

class WhatsAppService:
    @staticmethod
    def gerar_token():
        token = random.randint(1000, 9999)
        return token

    @staticmethod
    def enviar_codigo(numero, token):
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')

        cliente = Client(account_sid, auth_token)

        mensagem = f"Seu código de verificação é: {token}"

        cliente.messages.create(
            from_='whatsapp:+14155238886',
            body=mensagem,
            to=f'whatsapp:{numero}'
        )